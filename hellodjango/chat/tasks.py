from celery import shared_task
from .models import ChatMessage, ChatSession
from django.utils import timezone
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from langchain_core.prompts import ChatPromptTemplate
from langchain_huggingface import HuggingFaceEmbeddings
from openai import OpenAI
import os
from rag_service.rag_loader import vectorstore


import os
import logging
from celery import shared_task
from django.utils import timezone
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from openai import OpenAI

logger = logging.getLogger(__name__)


@shared_task
def generate_ai_reply(session_id, user_msg_id):
    """异步生成 AI 回复（带 RAG 自动降级 & 防止 UnboundLocalError"""
    from .serializers import ChatMessageSerializer  # 避免循环导入

    # 立刻初始化避免 UnboundLocalError
    prompt = None
    answer = None

    try:
        session = ChatSession.objects.get(id=session_id)
        user_msg = ChatMessage.objects.get(id=user_msg_id)
    except (ChatSession.DoesNotExist, ChatMessage.DoesNotExist) as e:
        logger.exception("session 或 user_msg 不存在: %s", e)
        return None

    # 用户问题（确保是字符串）
    question = (user_msg.content or "").strip()

    # 先假定不使用 RAG
    use_rag = False
    docs_content = ""

    # 尝试检索（如果 vectorstore 未初始化或检索失败则降级为普通模式）
    try:
        # 假设 vectorstore 是你全局已初始化的对象
        retrieved_docs = vectorstore.similarity_search(question, k=3)
        if retrieved_docs:
            docs_content = "\n\n".join(getattr(d, "page_content", str(d)) for d in retrieved_docs)
            # 仅当检索到有意义内容时启用 RAG
            if docs_content.strip():
                use_rag = True
    except Exception as e:
        # 记录错误但不抛出，直接降级为非 RAG
        logger.warning("RAG 检索失败，自动降级为直接问模型: %s", e)
        use_rag = False

    logger.info("RAG 是否启用: %s", use_rag)
    # 构造 prompt（确保 prompt 在任何路径都有值）
    if use_rag:
        prompt = f"""
            请根据下面的上下文信息回答问题。
            如果上下文不足以回答，请直接回答：“抱歉，我无法根据相关信息来回答此问题。”

            上下文:
            {docs_content}

            问题: {question}

            回答：
            """
    else:
        # 直接把 question 当作 prompt 发送给模型（简单模式）
        prompt = question or "你好，有什么我可以帮忙的吗？"

    # 日志记录以便排查
    logger.info("generate_ai_reply: session=%s, use_rag=%s, question=%s, prompt_length=%d",
                session_id, use_rag, question, len(prompt))

    # 调用模型
    try:
        client = OpenAI(
            api_key=os.getenv("DASHSCOPE_API_KEY"),
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        )

        completion = client.chat.completions.create(
            model="qwen-plus",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ],
            extra_body={"enable_thinking": False},
        )

        # 不同 SDK/版本返回结构可能不同，尝试几种安全的取法
        answer = None
        try:
            # 常见：completion.choices[0].message.content
            answer = completion.choices[0].message.content
        except Exception:
            try:
                # 有的 SDK 可能是 dict-like
                answer = completion.choices[0].message["content"]
            except Exception:
                try:
                    # 最后保底：如果是字符串化的整个对象
                    answer = getattr(completion, "text", None) or str(completion)
                except Exception:
                    answer = str(completion)

        if answer is None:
            answer = "抱歉，未能从模型获得有效回答。"

    except Exception as e:
        logger.exception("调用模型失败: %s", e)
        answer = "抱歉，AI 服务调用失败，请稍后重试。"

    # 保存 AI 回复
    assistant_msg = ChatMessage.objects.create(
        session=session,
        role='assistant',
        content=answer,
        created_at=timezone.now()
    )

    # 更新会话时间
    session.updated_at = assistant_msg.created_at
    session.save(update_fields=['updated_at'])

    # WebSocket 推送
    try:
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"chat_{session.id}", # ✅ 对应前端 WebSocket
            {
                "type": "chat_message", # ⚡ 对应 Consumer 的方法 chat_message
                "message": ChatMessageSerializer(assistant_msg).data
            }
        )
    except Exception as e:
        logger.exception("WebSocket 推送失败: %s", e)

    return ChatMessageSerializer(assistant_msg).data
