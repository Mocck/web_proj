from django.conf import settings
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework import status
from django.db import IntegrityError, transaction
from django.db.models import Q
from django.contrib.auth.hashers import make_password, check_password
from .models import User, Role, UserRole, LoginHistory, Team
from datetime import timedelta, datetime
from django.utils import timezone  # ✅ 这是 Django 的 timezone


from .serializers import (
    UserSerializer,
    RegisterSerializer,
    LoginSerializer,
    RoleSerializer,
    RegisterTeamSerializer,
    UserRoleSerializer,
    TeamSerializer
)

from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from django.middleware.csrf import get_token as get_csrf_token


def _get_tokens_for_user(user):
    refresh = RefreshToken()
    refresh['user_id'] = user.id  # 必须放 user_id，authenticate 时用
    access = refresh.access_token
    return {
        'refresh': str(refresh),
        'access': str(access),
    }


@api_view(['GET'])
@permission_classes([AllowAny])
@authentication_classes([])
def ping(request):
    return Response({"Hello Users!"})
    

@api_view(['POST'])
@permission_classes([AllowAny])  # ✅ 允许任何人访问（不需要 token）
@authentication_classes([])      # ✅ 禁用 JWT 验证
def register(request):
    # type(request.data) <class 'dict'>
    serializer = RegisterSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    input_data = serializer.validated_data
    
    # 防止同一用户名重复注册
    if User.objects.filter(username=input_data['username']).exists():
        return Response({'detail': 'username exists'}, status=status.HTTP_400_BAD_REQUEST)

    # 两次传入密码不一样
    if input_data['password'] != input_data['confirmpassword']:
        return Response({'detail': 'password is not same'}, status=status.HTTP_400_BAD_REQUEST)
    
    avatar_file = request.FILES.get('avatar')  # <--- 表单上传的图片文件
            
    try:
        user = User.objects.create(
            username=input_data['username'],
            email=input_data['email'],
            password=make_password(input_data['password']),  # ✅ 加密存储
            nickname=input_data.get('nickname', ''),
            phone_number=input_data['phone_number'],
            bio=input_data.get('bio', '')
        )

        if avatar_file:
            # if avatar uploaded, save it using Django's storage (ImageField)
            # user.avatar is an ImageField; calling save will store the file under MEDIA_ROOT
            user.avatar = avatar_file
            user.save()

    except IntegrityError as e:
        raise ValidationError(str(e))  # DRF 会调用 custom_exception_handler

    tokens = _get_tokens_for_user(user)
    output_data = serializer.data
    resp = Response({'detail': "register successful", 'user': UserSerializer(output_data).data, 'token': tokens}, status=status.HTTP_201_CREATED)
    
    # Cookie 设置
    access_lifetime = getattr(settings, 'SIMPLE_JWT', {}).get('ACCESS_TOKEN_LIFETIME', timedelta(minutes=30))
    refresh_lifetime = getattr(settings, 'SIMPLE_JWT', {}).get('REFRESH_TOKEN_LIFETIME', timedelta(days=7))
    access_max_age = int(access_lifetime.total_seconds())
    refresh_max_age = int(refresh_lifetime.total_seconds())
    secure_cookie = not settings.DEBUG  # 本地开发用 False

    resp.set_cookie(
        'access', tokens['access'],
        httponly=True,
        secure=secure_cookie,
        samesite='Lax',
        max_age=access_max_age
    )
    resp.set_cookie(
        'refresh', tokens['refresh'],
        httponly=True,
        secure=secure_cookie,
        samesite='Lax',
        max_age=refresh_max_age
    )

    # DEBUG 下返回 token 方便调试
    if settings.DEBUG:
        resp.data['token'] = tokens

    return resp


# Celery定时解锁 locked user
from celery import shared_task

LOCK_DURATION = timedelta(minutes=30)

@shared_task
def unlock_locked_users():
    # 自动根据 USE_TZ / TIME_ZONE 设置决定返回值
    now = datetime.now()

    users = User.objects.filter(is_locked=True, locked_at__lte=now-LOCK_DURATION)

    for user in users:
        user.is_locked = False
        user.failed_login_attempts = 0
        user.locked_at = None
        user.save(update_fields=['is_locked','failed_login_attempts','locked_at'])


@api_view(['POST'])
@permission_classes([AllowAny])
@authentication_classes([])
@transaction.atomic
def login(request):
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    data = serializer.validated_data

    key = data['username_or_email']
    password = data['password']

    user = User.objects.filter(Q(username=key) | Q(email=key)).first()

    if user.is_locked:
        return Response({'detail': 'user is locking'}, status=status.HTTP_403_FORBIDDEN)
    
    if not user or not check_password(password, user.password):
        if user:
            user.failed_login_attempts = (user.failed_login_attempts or 0) + 1
            user.save(update_fields=['failed_login_attempts'])

            if user.failed_login_attempts >= 5:
                user.is_locked = True

                # 是 Django 提供的 django.utils.timezone，而是 Python 内置的 datetime.timezone 模块，所以它没有 .now() 方法。
                user.locked_at = timezone.now()

                user.save(update_fields=['is_locked', 'locked_at'])
                return Response({'detail': 'password error beyond max try'}, status=status.HTTP_400_BAD_REQUEST)
            
            return Response({'detail': 'invalid password'}, status=status.HTTP_400_BAD_REQUEST)
        else: 
            return Response({'detail': 'user not exist'}, status=status.HTTP_400_BAD_REQUEST)
    
    if not user.is_active:
        return Response({'detail': 'user inactive'}, status=status.HTTP_403_FORBIDDEN)

    # 获取客户端 IP 的辅助函数
    def get_client_ip(request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR', '')
        return ip
    
    # 保存登录历史
    ip_address = get_client_ip(request)
    device_info = request.META.get('HTTP_USER_AGENT', 'unknown')
    LoginHistory.objects.create(
        user=user,
        ip_address=ip_address,
        device_info=device_info
    )

    # 生成 token
    tokens = _get_tokens_for_user(user)

    # Cookie 设置
    resp = Response({'user': UserSerializer(user).data, 'detail': 'login successful', 'token': tokens})

    access_lifetime = getattr(settings, 'SIMPLE_JWT', {}).get('ACCESS_TOKEN_LIFETIME', timedelta(minutes=30))
    refresh_lifetime = getattr(settings, 'SIMPLE_JWT', {}).get('REFRESH_TOKEN_LIFETIME', timedelta(days=7))
    access_max_age = int(access_lifetime.total_seconds())
    refresh_max_age = int(refresh_lifetime.total_seconds())
    secure_cookie = not settings.DEBUG  # 本地开发用 False

    resp.set_cookie(
        'access', tokens['access'],
        httponly=True,
        secure=secure_cookie,
        samesite='Lax',
        max_age=access_max_age
    )
    resp.set_cookie(
        'refresh', tokens['refresh'],
        httponly=True,
        secure=secure_cookie,
        samesite='Lax',
        max_age=refresh_max_age
    )

    # DEBUG 下返回 token 方便调试
    if settings.DEBUG:
        resp.data['token'] = tokens

    return resp


@api_view(['POST'])
@permission_classes([AllowAny])
@authentication_classes([])
def logout(request):
    """Logout endpoint.

    Expect POST body: { "refresh": "<refresh_token>" }
    If server has simplejwt blacklist app enabled, this will blacklist the refresh token.
    Otherwise the client should simply delete stored tokens.
    """
    # Prefer refresh token from cookie (cookie-based auth), else accept from body
    refresh_token = request.COOKIES.get('refresh') or request.data.get('refresh')

    # Build response that will delete cookies on client side.
    # Use the same path/samesite as when setting the cookie to ensure deletion works.
    resp = Response({'detail': 'logged out'}, status=status.HTTP_200_OK)
    # delete access and refresh cookies (these were set with samesite='Lax' and path default '/')
    resp.delete_cookie('access', path='/', samesite='Lax')
    resp.delete_cookie('refresh', path='/', samesite='Lax')
    # also clear csrf cookie if present (frontend may store csrftoken cookie)
    resp.delete_cookie('csrftoken', path='/', samesite='Lax')

    if not refresh_token:
        # no token to blacklist; instruct client to remove tokens
        resp.data = {'detail': 'no refresh token provided; cookies cleared on server; delete tokens on client side'}
        return resp

    try:
        token = RefreshToken(refresh_token)
    except TokenError:
        resp.data = {'detail': 'invalid refresh token; cookies cleared'}
        return resp

    # Try to blacklist (requires rest_framework_simplejwt.token_blacklist in INSTALLED_APPS)
    try:
        token.blacklist()
        resp.data = {'detail': 'logout successful; token blacklisted'}
        return resp
    except AttributeError:
        # blacklist not enabled
        resp.data = {'detail': 'server does not support blacklisting; cookies cleared'}
        return resp
    except Exception:
        resp.data = {'detail': 'failed to logout; cookies cleared'}
        return resp

# 用户菜单
'''
Response = [
  {
    "id": 1,
    "name": "管理",
    "children": [
      { "id": 101, "name": "用户管理", "path": "/user" },
      { "id": 102, "name": "角色管理", "path": "/role" }
    ]
  },
  {
    "id": 2,
    "name": "报表",
    "children": [
      { "id": 201, "name": "销售报表", "path": "/sales" },
      { "id": 202, "name": "库存报表", "path": "/inventory" }
    ]
  }
]

'''
@api_view(["GET"])
def menu(request):
    # 使用 request.user 判断是否登录
    user = request.user
    role_id = user.user_roles

    # role = 5 可见菜单
    menus = [
        {
            "id": 1,
            "name": "个人管理",
            "children": [
            { "id": 101, "name": "用户管理", "path": "/me" }
            ]
        },
        {
            "id": 2,
            "name": "团队管理",
            "children": [
            { "id": 201, "name": "创建团队", "path": "/create_team" }
            ]
        }
    ]

    if role_id == 4:
        menus += [
            {
                "id": 3,
                "name": "团队管理",
                "children": [
                { "id": 201, "name": "创建团队", "path": "/teams" }
                ]
            }
        ]
    if role_id == 3:
        menus += [

        ]
    if role_id == 2:
        menus += [

        ]
    if role_id == 1:
        menus += [

        ]

    return Response(menus, status=status.HTTP_200_OK)




# 用户个人管理
@api_view(['GET', 'PUT', 'DELETE'])
def user_detail(request):
    user = request.user

    if request.method == 'GET':
        return Response(UserSerializer(user).data)

    if request.method == 'PUT':
        data = request.data
        # only allow certain fields to be updated
        updatable = ['nickname', 'email', 'phone_number', 'avatar', 'bio', 'is_active']
        changed = False
        for f in updatable:
            if f in data:
                setattr(user, f, data[f])
                changed = True
        if changed:
            user.save()
        return Response(UserSerializer(user).data)

    if request.method == 'DELETE':
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def users_list(request):
    """用户列表：支持分页 page, page_size, 和模糊搜索 q"""
    q = request.GET.get('q', '').strip()
    page = int(request.GET.get('page', 1))
    page_size = int(request.GET.get('page_size', 10))

    qs = User.objects.all().order_by('-created_at')
    if q:
        qs = qs.filter(Q(username__icontains=q) | Q(email__icontains=q) | Q(nickname__icontains=q))

    total = qs.count()
    start = (page - 1) * page_size
    end = start + page_size
    rows = qs[start:end]
    serializer = UserSerializer(rows, many=True)
    return Response({'total': total, 'page': page, 'page_size': page_size, 'items': serializer.data})


@api_view(['POST'])
def assign_role(request):
    """为用户分配角色：body 包含 user_id, role_id, 可选 team_id"""
    user_id = request.data.get('user_id')
    role_id = request.data.get('role_id')
    team_id = request.data.get('team_id')

    if not user_id or not role_id:
        return Response({'detail': 'user_id and role_id required'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        user = User.objects.get(id=user_id)
        role = Role.objects.get(id=role_id)
    except (User.DoesNotExist, Role.DoesNotExist):
        return Response({'detail': 'user or role not found'}, status=status.HTTP_404_NOT_FOUND)

    # create or update
    ur, created = UserRole.objects.get_or_create(user=user, role=role, defaults={'team_id': team_id} if team_id else {})
    if not created and team_id:
        ur.team_id = team_id
        ur.save()

    return Response(UserRoleSerializer(ur).data)


@api_view(['GET'])
def get_user_roles(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({'detail': 'user not found'}, status=status.HTTP_404_NOT_FOUND)
    urs = UserRole.objects.filter(user=user)
    serializer = UserRoleSerializer(urs, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([AllowAny])
@authentication_classes([])
def csrf(request):
    """Return CSRF token and ensure CSRF cookie is set.

    Frontend should GET this endpoint to obtain CSRF token, then send it in
    the 'X-CSRFToken' header for subsequent unsafe requests (POST/PUT/DELETE).
    """
    token = get_csrf_token(request)
    return Response({'csrfToken': token})


# 团队管理
@api_view(['POST'])
def create_team(request):
    # 读取创建用户
    user = request.user
    user_id = user.id  # 直接拿 user_id
    # 序列化传入表单
    serializer = RegisterTeamSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    input_data = serializer.validated_data
    
    avatar_file = request.FILES.get('avatar')  

    try:
        team = Team.objects.create(
            name=input_data['name'],
            owner_id=user_id,
            is_public=input_data['is_public'],
            join_policy=input_data['join_policy'],
            max_members=input_data['max_members'],
            description=input_data.get('description', '')
        )
        if avatar_file:
            team.avatar = avatar_file
            team.save()

    except IntegrityError as e:
        raise ValidationError(str(e))

    output_data = serializer.data
    return Response({'detail': 'Team created successfully', 'team': output_data}, status=status.HTTP_201_CREATED)