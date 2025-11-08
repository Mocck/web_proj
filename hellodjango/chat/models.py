from django.db import models
from django.conf import settings


class ChatSession(models.Model):
    id = models.BigAutoField(primary_key=True, db_column='id')
    user = models.ForeignKey(        # ✅ 改成 user
        'user_management.User',
        on_delete=models.RESTRICT,
        db_column='user_id',
        related_name='sessions',  # 反向访问用：request.user.sessions.all()
        verbose_name='所属用户'
    )
    title = models.CharField(max_length=100, null=True, blank=True, verbose_name='会话标题')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    is_deleted = models.BooleanField(default=False, verbose_name='是否删除')

    class Meta:
        db_table = 'chat_session'
        verbose_name = '聊天会话'
        managed = False

    def __str__(self):
        return f"{self.title or '(无标题)'}"


class ChatMessage(models.Model):
    id = models.BigAutoField(primary_key=True, db_column='id')
    session = models.ForeignKey(
        ChatSession,
        on_delete=models.CASCADE,
        db_column='session_id',
        related_name='messages',
        verbose_name='会话ID'
    )
    role = models.CharField(max_length=20, verbose_name='角色（user/assistant/system）')
    content = models.TextField(verbose_name='消息内容')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='发送时间')

    class Meta:
        db_table = 'chat_message'
        verbose_name = '聊天消息'
        managed = False

    def __str__(self):
        return f"[{self.role}] {self.content[:30]}"
