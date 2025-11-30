from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    # 用户管理系统 /api/users/ 测试连通
    path('', views.ping),

    # 注册
    path('register/', views.register, name='um_register'),

    # standard JWT endpoints (optional)
    path('token/', views.get_token, name='token_obtain'),
    path('token/refresh/', views.refresh_token, name='token_refresh'),
    
    # 登录
    path('login/', views.login, name='um_login'),
    path('logout/', views.logout, name='um_logout'),
    # CSRF token endpoint for cookie-based auth
    path('csrf/', views.csrf, name='um_csrf'),
    
    # 用户个人管理：查看
    path('me/', views.user_detail, name='user_detail'),
    # 用户个人管理：更新
    path('me/update/', views.user_update, name='user_update'),
    # 用户个人管理：删除
    path('me/delete/', views.user_delete, name='user_delete'),
    # 修改密码
    path('password/', views.change_password, name='chage_password'),

    # 主页菜单展示
    path('menus/',views.menu, name='user_menu'),

    
    # 为用户分配角色
    path('roles/assign/', views.assign_role, name='assign_role'),
    path('users/<int:user_id>/roles/', views.get_user_roles, name='user_roles'),
    # 创建团队
    path('create_team/', views.create_team, name='create_team'),
    # path('teams/', views.create_team, name='create_team'),

    # 管理用户
    # path('manage_users/',)
    
]
