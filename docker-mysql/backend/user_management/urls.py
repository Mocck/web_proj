from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    # 用户管理系统 /api/users/ 测试连通
    path('', views.ping),

    # 注册
    path('register/', views.register, name='um_register'),

    # standard JWT endpoints (optional)
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # 登录
    path('login/', views.login, name='um_login'),
    path('logout/', views.logout, name='um_logout'),
    # CSRF token endpoint for cookie-based auth
    path('csrf/', views.csrf, name='um_csrf'),
    
    # 用户个人管理：查看、更新、删除
    path('me/', views.user_detail, name='user_detail'),
    
    # 主页菜单展示
    path('menus/',views.menu, name='user_menu'),

    # 用户列表展示
    path('users_list/', views.users_list, name='users_list'),
    
    # 为用户分配角色
    path('roles/assign/', views.assign_role, name='assign_role'),
    path('users/<int:user_id>/roles/', views.get_user_roles, name='user_roles'),

    # 团队管理
    path('teams/', views.create_team, name='create_team'),
    
]
