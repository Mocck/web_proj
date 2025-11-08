from django.db import models


class User(models.Model):
    id = models.BigAutoField(primary_key=True)
    username = models.CharField(max_length=100, unique=True, verbose_name="用户名")
    email = models.EmailField(max_length=128, unique=True, verbose_name="邮箱")
    phone_number = models.CharField(max_length=15, unique=True, blank=True, null=True, verbose_name="手机号")
    password = models.CharField(max_length=256, verbose_name="密码")
    confirmpassword = models.CharField(max_length=256, verbose_name='确认密码')
    # 以下字段自动生成 default
    nickname = models.CharField(max_length=64, blank=True, null=True, verbose_name="昵称")
    avatar = models.ImageField(upload_to='avatars/', max_length=255, blank=True, null=True, verbose_name="头像")
    bio = models.TextField(blank=True, null=True, verbose_name="个人简介")
    
    # 暂时停用用户，通常用于标记用户是否可以登录或使用系统功能。例如：未激活的用户可能是刚注册但未验证邮箱的用户。
    is_active = models.BooleanField(default=True, verbose_name="是否激活")  
    # 通常用于安全目的，例如五次登录失败后锁定账户。锁定的用户可能需要管理员手动解锁或等待一段时间后自动解锁。
    is_locked = models.BooleanField(default=False, verbose_name="是否锁定")
    failed_login_attempts = models.IntegerField(default=0, verbose_name="登录失败次数")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    locked_at = models.DateTimeField(verbose_name="锁定时间")

    class Meta:
        db_table = 't_user'
        verbose_name = "用户"
        verbose_name_plural = "用户"
        indexes = [
            models.Index(fields=['username'], name='idx_username'),
        ]

    def __str__(self):
        return self.username

class LoginHistory(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='login_histories', verbose_name="用户")
    login_time = models.DateTimeField(auto_now_add=True, verbose_name="登录时间")
    ip_address = models.GenericIPAddressField(verbose_name="IP地址")
    device_info = models.CharField(max_length=256, verbose_name="设备信息")

    class Meta:
        db_table = 't_login_history'
        verbose_name = "登录历史"
        verbose_name_plural = "登录历史"
        indexes = [
            models.Index(fields=['user'], name='idx_user'),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.login_time}"

class Team(models.Model):
    id = models.BigAutoField(primary_key=True, verbose_name="团队ID")
    name = models.CharField(max_length=100, unique=True, verbose_name="团队名称")
    description = models.TextField(blank=True, null=True, verbose_name="团队描述")
    avatar = models.CharField(max_length=500, blank=True, null=True, verbose_name="团队头像URL")
    
    # 可见性：public-1，private-0
    is_public = models.CharField(max_length=20, default='private', verbose_name="可见性")
    
    # 加入策略：open-开放，approval-需审批，invite-仅邀请
    join_policy = models.CharField(max_length=20, default='approval', verbose_name="加入策略")
    
    max_members = models.IntegerField(blank=True, null=True, verbose_name="最大成员数")
    
    owner = models.ForeignKey(
        'User',  
        on_delete=models.RESTRICT,
        db_column='owner_id',
        verbose_name="团队负责人"
    )
    
    status = models.SmallIntegerField(default=1, verbose_name="状态")  # 0-禁用，1-正常，2-已解散
    
    settings = models.JSONField(blank=True, null=True, verbose_name="团队设置")  # Django 3.1+ 内置 JSONField
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    deleted_at = models.DateTimeField(blank=True, null=True, verbose_name="删除时间（软删除）")

    class Meta:
        db_table = 't_team'
        verbose_name = "团队"
        verbose_name_plural = "团队"
        indexes = [
            models.Index(fields=['owner'], name='idx_owner_id'),
            models.Index(fields=['is_public'], name='idx_visibility'),
            models.Index(fields=['status'], name='idx_status'),
            models.Index(fields=['created_at'], name='idx_created_at'),
            models.Index(fields=['deleted_at'], name='idx_deleted_at'),
        ]

    def __str__(self):
        return self.name


class Role(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=64, unique=True, verbose_name="角色名称")
    description = models.CharField(max_length=256, blank=True, null=True, verbose_name="角色描述")
    scope = models.CharField(max_length=32, choices=[('system', '系统'), ('team', '团队'), ('user', '个人')], verbose_name="角色作用域")
    sort_order = models.IntegerField(default=0, verbose_name="权限等级")

    class Meta:
        db_table = 't_role'
        verbose_name = "角色"
        verbose_name_plural = "角色"

    def __str__(self):
        return self.name

class Permission(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=64, unique=True, verbose_name="权限名称")
    code = models.CharField(max_length=64, unique=True, verbose_name="权限编码")
    description = models.CharField(max_length=256, blank=True, null=True, verbose_name="权限描述")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        db_table = 't_permission'
        verbose_name = "权限"
        verbose_name_plural = "权限"

    def __str__(self):
        return self.name

class UserRole(models.Model):
    id = models.BigAutoField(primary_key=True)

    '''
        外键字段 models.ForeignKey(...) 已经对应数据库的 user_id
        related_name='user_roles', 给 User 模型反向访问当前表用的名字。
        user.user_roles.all() 可以获取这个用户的对应信息。
    '''
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='user_roles', verbose_name="用户")
    role = models.ForeignKey('Role', on_delete=models.CASCADE, related_name='role_users', verbose_name="角色")
    team = models.ForeignKey('Team', on_delete=models.CASCADE, blank=True, null=True, related_name='team_roles', verbose_name="团队")

    class Meta:
        db_table = 't_user_role'
        verbose_name = "用户角色关联"
        verbose_name_plural = "用户角色关联"

    def __str__(self):
        return f"{self.user.username} - {self.role.name}"

class RolePermission(models.Model):
    id = models.BigAutoField(primary_key=True)
    role = models.ForeignKey('Role', on_delete=models.CASCADE, related_name='role_permissions', verbose_name="角色")
    permission = models.ForeignKey('Permission', on_delete=models.CASCADE, related_name='permission_roles', verbose_name="权限")

    class Meta:
        db_table = 't_role_permission'
        verbose_name = "角色权限关联"
        verbose_name_plural = "角色权限关联"

    def __str__(self):
        return f"{self.role.name} - {self.permission.name}"

class DataPermission(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='data_permissions', verbose_name="用户")
    data_scope = models.CharField(max_length=128, verbose_name="数据访问范围")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        db_table = 't_data_permission'
        verbose_name = "数据权限"
        verbose_name_plural = "数据权限"

    def __str__(self):
        return f"{self.user.username} - {self.data_scope}"