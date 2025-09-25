from rest_framework import serializers
from agents.models import Agent

class AgentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agent
        fields = '__all__'  # 只暴露想给前端看的字段