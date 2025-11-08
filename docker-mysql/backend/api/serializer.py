from rest_framework import serializers
from agents.models import Agent
from graph.models import Graph
from workspace.models import WorkSpace
from user_management.models import User, LoginHistory, Team, Role, Permission, UserRole, RolePermission, DataPermission

class AgentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agent
        fields = '__all__'  # 只暴露想给前端看的字段

class GraphSerializer(serializers.ModelSerializer):
    class Meta:
        model = Graph
        fields = '__all__' 

class WorkSpaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkSpace
        fields = '__all__'  

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__' 

class LoginHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = LoginHistory
        fields = '__all__' 

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = '__all__' 

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__' 

class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = '__all__' 

class UserRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRole
        fields = '__all__' 

class RolePermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = RolePermission
        fields = '__all__' 

class DataPermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataPermission
        fields = '__all__' 