from celery import shared_task
from .models import ChatMessage, ChatSession
from django.utils import timezone
import time
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

@shared_task
def generate_ai_reply(session_id, user_msg_id):
    """异步生成 AI 回复"""
    from .serializers import ChatMessageSerializer  # 避免循环导入

    try:
        session = ChatSession.objects.get(id=session_id)
        user_msg = ChatMessage.objects.get(id=user_msg_id)
    except (ChatSession.DoesNotExist, ChatMessage.DoesNotExist):
        return None

    # 💤 模拟 AI 生成耗时
    time.sleep(3)

    # 假设生成的回复内容
    ai_content = f"这是AI针对你的消息“{user_msg.content}”生成的回复"

    # 保存 AI 回复
    assistant_msg = ChatMessage.objects.create(
        session=session,
        role='assistant',
        content=ai_content,
        created_at=timezone.now()
    )

    # 更新会话时间
    session.updated_at = assistant_msg.created_at
    session.save(update_fields=['updated_at'])

    # # WebSocket 推送
    # channel_layer = get_channel_layer()
    # async_to_sync(channel_layer.group_send)(
    #     f"chat_{session.user.id}",  # 每个用户一个 group
    #     {
    #         "type": "chat.message",
    #         "message": ChatMessageSerializer(ai_msg).data
    #     }
    # )

    return ChatMessageSerializer(assistant_msg).data


