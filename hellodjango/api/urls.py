from django.urls import path
from . import views

urlpatterns = [
    path('ping/', views.ping),
    path("apps/", views.apps),
    path("graph/", views.graph),
    path("workspace/", views.space),
]
