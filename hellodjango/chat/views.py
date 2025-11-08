from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import ChatSession, ChatMessage
from .serializers import ChatSessionSerializer, ChatMessageSerializer
from .tasks import generate_ai_reply  # 导入 Celery 异步任务


# 创建会话
@api_view(['POST'])
def create_session(request):
    title = request.data.get('title', '新会话')
    session = ChatSession.objects.create(user=request.user, title=title)
    return Response(ChatSessionSerializer(session).data, status=status.HTTP_201_CREATED)


# 列出我的会话
@api_view(['GET'])
def list_sessions(request):
    sessions = ChatSession.objects.filter(user=request.user, is_deleted=False).order_by('-updated_at')
    return Response(ChatSessionSerializer(sessions, many=True).data)


# 删除会话
@api_view(['DELETE'])
def delete_session(request, id):
    try:
        session = ChatSession.objects.get(id=id, user=request.user)
        session.is_deleted = True
        session.save(update_fields=['is_deleted'])
        return Response({'detail': '会话已删除'}, status=status.HTTP_200_OK)
    except ChatSession.DoesNotExist:
        return Response({'detail': '会话不存在'}, status=status.HTTP_404_NOT_FOUND)


# ✅ 查询某个session的全部message， GET /api/chat/messages/?sessionId=3
@api_view(['GET'])
def list_messages(request):
    session_id = request.query_params.get('session_id')  # ✅ 从URL参数取
    if not session_id:
        return Response({'detail': '缺少 session_id'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        # ✅ 校验会话是否属于当前用户， user=request.user
        session = ChatSession.objects.get(id=session_id, user=request.user)
    except ChatSession.DoesNotExist:
        return Response({'detail': '会话不存在或无权限'}, status=status.HTTP_404_NOT_FOUND)

    messages = ChatMessage.objects.filter(session=session).order_by('created_at')
    return Response(ChatMessageSerializer(messages, many=True).data)


# ✅ 发送消息（user -> assistant）
@api_view(['POST'])
def send_message(request):
    session_id = request.data.get('session_id')
    content = request.data.get('content')
    if not (session_id and content):
        return Response({'detail': '缺少参数'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        session = ChatSession.objects.get(id=session_id, user=request.user)
    except ChatSession.DoesNotExist:
        return Response({'detail': '会话不存在或无权限'}, status=status.HTTP_404_NOT_FOUND)

    # ✅ 保存用户消息
    user_msg = ChatMessage.objects.create(session=session, role='user', content=content)
    session.updated_at = user_msg.created_at
    session.save(update_fields=['updated_at'])

    # ✅ 异步生成 AI 回复
    generate_ai_reply.delay(session.id, user_msg.id)

    # ✅ 立即返回，前端可提示“正在生成”
    return Response({
        'status': 'processing',
        'message': 'AI 正在生成回复中',
        'user_message': ChatMessageSerializer(user_msg).data
    }, status=status.HTTP_202_ACCEPTED)
