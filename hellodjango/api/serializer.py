from rest_framework import serializers
from agents.models import Agent
from graph.models import Graph
from workspace.models import WorkSpace

class AgentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agent
        fields = '__all__'  # 只暴露想给前端看的字段

class GraphSerializer(serializers.ModelSerializer):
    class Meta:
        model = Graph
        fields = '__all__'  # 只暴露想给前端看的字段

class WorkSpaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkSpace
        fields = '__all__'  # 只暴露想给前端看的字段
