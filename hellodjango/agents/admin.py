from django.contrib import admin

# Register your models here.
from .models import Agent   
admin.site.register(Agent)  # 注册模型到 admin 后台
