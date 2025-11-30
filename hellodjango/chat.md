# 创建会话
@api_view(['POST'])
def create_session(request):
    {
        'title':'新会话'
    }

# 列出我的会话
@api_view(['GET'])
def list_sessions(request):

# 删除会话
@api_view(['DELETE'])
def delete_session(request, id):


# ✅ 查询某个session的全部message， GET /api/chat/messages/?sessionId=3
@api_view(['GET'])
def list_messages(request):


# ✅ 发送消息（user -> assistant）
@api_view(['POST'])
def send_message(request):
    {
    "session_id":"3",
    "content":"这是一个测试"
    }

# ✅ 异步任务生成 AI 回复

```python
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

    return ChatMessageSerializer(assistant_msg).data

```

✅ 推荐配置


```bash
celery -A HelloWorld worker -l info
celery -A HelloWorld beat -l info
```


| 模式            | 特点      | Windows兼容      | 说明             |
| ------------- | ------- | -------------- | -------------- |
| `prefork`（默认） | 多进程高并发  | ❌ 不稳定          | 需要 Unix fork   |
| `solo`        | 单进程串行执行 | ✅ 完全兼容         | 稳定、安全，适合后台定时任务 |
| `threads`     | 多线程     | ⚠️ 可用但有 GIL 限制 | 可替代但性能有限       |

💡 怎么让它“并发”一点？

## 在 Windows 下 Celery 没有真正多进程的 prefork 模式，但你有几个可行的替代方案：

- ✅ 方案 1：开多个 worker 实例（伪并行）

可以同时开两个独立 worker 进程（命令行窗口）：

```bash
celery -A HelloWorld worker --pool=solo -l info 
celery -A HelloWorld worker --pool=solo -l info
```


这样 Celery 会分配任务到不同 worker，相当于多进程并发执行。
（只是你手动启动两个进程）

- ✅ 方案 2：使用 --pool=threads
celery -A HelloWorld worker --pool=threads -c 4 -l info


线程池可让同一进程中同时执行多个任务；

对 I/O 密集型（例如网络请求、数据库操作）比较有效；

对 CPU 密集型（例如深度计算）帮助不大。


# 安装 Channels 和 Redis 支持
pip install channels channels_redis

# 运行 ASGI 服务器
使用 uvicorn HelloWorld.asgi:application --host localhost --port 8080