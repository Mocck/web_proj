from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# 设置默认 Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HelloWorld.settings')

app = Celery('HelloWorld')

# 从 Django settings 读取 Celery 配置（以 CELERY_ 开头）
app.config_from_object('django.conf:settings', namespace='CELERY')

# 自动发现所有 app 下的 tasks.py
app.autodiscover_tasks()


from celery.schedules import crontab

app.conf.beat_schedule = {
    'unlock-locked-users-every-30-mins': {
        'task': 'user_management.tasks.unlock_locked_users',
        'schedule': crontab(minute='*/30'),  # 每 30 分钟
    },
}