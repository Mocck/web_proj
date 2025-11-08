# user_management/tasks.py
from celery import shared_task
from datetime import datetime, timedelta
from .models import User

# Celery定时解锁 locked user
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
