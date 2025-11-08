from django.http import HttpResponse, JsonResponse
import time


def hello(request):
    return HttpResponse("Hello django!")
