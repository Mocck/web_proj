from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import exceptions, status
from rest_framework.exceptions import AuthenticationFailed
from .models import User
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.utils import get_md5_hash_password
from django.utils.translation import gettext_lazy as _


class CookieOrHeaderJWTAuthentication(JWTAuthentication):
    """Authenticate by Authorization header first, then fall back to access token cookie.

    This allows browser clients to use HttpOnly cookies while still supporting
    non-browser clients that send Authorization: Bearer <token>.
    """
        
    def get_user(self, validated_token):
        user_id = validated_token.get("user_id")

        if not user_id:
            raise AuthenticationFailed(_("Invalid token: no user_id"), code=status.HTTP_401_UNAUTHORIZED)

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise AuthenticationFailed(_("User not found"), code=status.HTTP_401_UNAUTHORIZED)

        # ✅ 检查是否激活
        if getattr(api_settings, "CHECK_USER_IS_ACTIVE", True) and not user.is_active:
            raise AuthenticationFailed(_("User is inactive"), code=status.HTTP_401_UNAUTHORIZED)

        # ✅ 检查密码修改后 token 是否应失效
        if getattr(api_settings, "CHECK_REVOKE_TOKEN", False):
            revoke_claim = validated_token.get(getattr(api_settings, "REVOKE_TOKEN_CLAIM", "revoke_token"))
            if revoke_claim and revoke_claim != get_md5_hash_password(user.password):
                raise AuthenticationFailed(_("Password has changed."), code=status.HTTP_401_UNAUTHORIZED)

        return user
    
    
    def authenticate(self, request):
        # Try standard header-based authentication first
        header_auth = super().authenticate(request)
        if header_auth is not None:
            return header_auth

        # Fallback: read token from cookie named 'access'
        raw_token = request.COOKIES.get('access')
        if not raw_token:
            return None

        try:
            validated_token = self.get_validated_token(raw_token)
            user = self.get_user(validated_token)
            return (user, validated_token)
        except exceptions.AuthenticationFailed:
            raise
        except Exception:
            # any other issue treat as no authentication
            return None
        

from rest_framework.permissions import BasePermission

class IsCustomAuthenticated(BasePermission):
    def has_permission(self, request, views):
        return bool(request.user and request.user.id)  # 用 id 判断已认证
