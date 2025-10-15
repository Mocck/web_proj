from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .common.response import ApiResponse
from .common.handlers import BusinessException
from datetime import date
from decimal import Decimal
from agents.models import Agent
from graph.models import Graph
from workspace.models import WorkSpace
from .serializer import AgentSerializer, GraphSerializer, WorkSpaceSerializer

from asgiref.sync import sync_to_async

@sync_to_async
def get_data(mymodel):
    return list(mymodel.objects.all())

@api_view(['GET'])  
def ping(request):
    return Response(ApiResponse.ok({"msg": "pong"}).dict())


async def apps(request):
    rows = await get_data(Agent)  # ORM 查询所有数据
    serializer = AgentSerializer(rows, many=True) # 把 QuerySet 直接作为 instance

    # 对 .data 按照评分处理
    sorted_data = sorted(serializer.data, key=lambda x:x['rating'], reverse=True)

    # 对 .data 按照下载量处理
    # sorted_data = sorted(serializer.data, key=lambda x:x['downloads'], reverse=True)

    return JsonResponse(sorted_data, safe=False)    # 取出序列化后的数据, .data属性才是 DRF 已经转换好的 Python 原生数据结构（list[dict]），Response 会自动再转成 JSON。
    
@api_view(['GET'])
def graph(request):
    rows = Graph.objects.all()
    serializer = GraphSerializer(rows, many=True) # 把 QuerySet 直接作为 instance
    return Response(serializer.data)

@api_view(['GET'])
def space(request):
    rows = WorkSpace.objects.all()
    serializer = WorkSpaceSerializer(rows, many=True) # 把 QuerySet 直接作为 instance
    return Response(serializer.data)