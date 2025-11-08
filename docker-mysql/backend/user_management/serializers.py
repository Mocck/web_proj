from rest_framework import serializers
from .models import User, Role, UserRole, Team

# 用户信息序列化
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username', 'email', 'nickname', 'avatar', 'bio',
            'is_active', 'is_locked', 'failed_login_attempts', 'created_at', 'updated_at'
        ]

# 注册信息序列化
class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    email = serializers.EmailField(max_length=128)
    password = serializers.CharField(write_only=True)
    confirmpassword = serializers.CharField(write_only=True)
    nickname = serializers.CharField(max_length=64, required=False, allow_blank=True)
    phone_number = serializers.CharField(max_length=15)

# 登录信息序列化
class LoginSerializer(serializers.Serializer):
    username_or_email = serializers.CharField()
    password = serializers.CharField(write_only=True)

# 团队注册信息
class RegisterTeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['name', 'is_public', 'join_policy', 'max_members', 'description', 'avatar']

# 团队信息
class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username', 'email', 'nickname', 'avatar', 'bio',
            'is_active', 'is_locked', 'failed_login_attempts', 'created_at', 'updated_at'
        ]

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 'name', 'description', 'scope', 'created_at']


class UserRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRole
        fields = ['id', 'user', 'role', 'team']
