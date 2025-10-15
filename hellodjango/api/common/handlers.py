from rest_framework.views import exception_handler
from rest_framework.response import Response
from django.http import Http404
from django.core.exceptions import BadRequest
from rest_framework.exceptions import ValidationError
from .response import ApiResponse
import traceback
import logging
logger = logging.getLogger(__name__)


# 自定义业务异常
class BusinessException(Exception):
    def __init__(self, code: int, message: str):
        super().__init__(message)
        self.code = code
        self.message = message

# DRF 全局异常处理器
def custom_exception_handler(exc, context):
    if isinstance(exc, BusinessException):
        return Response(ApiResponse.fail(exc.code, exc.message).dict())
    
    if isinstance(exc, (BadRequest, ValidationError)):
        return Response(ApiResponse.fail(40000, str(exc)).dict())
    
    if isinstance(exc, Http404):
        request = context.get("request")
        path = request.path if request else ""
        return Response(ApiResponse.fail(40400, f"资源不存在: {path}").dict(), status=404)

    response = exception_handler(exc, context)
    if response is not None:
        return Response(ApiResponse.fail(response.status_code * 100, response.data).dict())

    '''# ✅ 打印堆栈，方便排查 50000 错误
    traceback.print_exc()
    logger.exception("Unhandled exception in DRF:")
    '''

    return Response(ApiResponse.fail(50000, "服务器异常，请稍后再试").dict(), status=500)


# Django URL 404 handler
from django.http import JsonResponse

def custom_page_not_found(request, exception=None):
    return JsonResponse({"code": 404, "msg": "page not found"}, status=404)

