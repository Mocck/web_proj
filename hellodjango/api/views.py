from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .common.response import ApiResponse
from .common.handlers import BusinessException
from agents.apps import AppVO
from datetime import date
from decimal import Decimal
from dataclasses import asdict
from agents.models import Agent
from .serializer import AgentSerializer

@api_view(['GET'])  
def ping(request):
    return Response(ApiResponse.ok({"msg": "pong"}).dict())


@api_view(['GET'])
def apps(request):
    rows = Agent.objects.all()  # ORM 查询所有数据
    serializer = AgentSerializer(rows, many=True) # 把 QuerySet 直接作为 instance
    return Response(serializer.data)    # 取出序列化后的数据, .data属性才是 DRF 已经转换好的 Python 原生数据结构（list[dict]），Response 会自动再转成 JSON。
    