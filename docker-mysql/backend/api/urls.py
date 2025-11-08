from django.urls import path, include
from . import views

urlpatterns = [
    path('ping/', views.ping),
    path("apps/", views.apps),
    path("graph/", views.graph),
    path("workspace/", views.space),
    # 用户管理系统
    path('users/', include('user_management.urls')),
]
