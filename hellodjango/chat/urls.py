from django.urls import path
from . import views

urlpatterns = [
    path('sessions/', views.list_sessions, name='chat_sessions'),
    path('sessions/create/', views.create_session, name='chat_create'),
    path('sessions/<int:id>/', views.delete_session, name='chat_delete'),
    path('messages/', views.list_messages, name='chat_messages'),
    path('messages/send/', views.send_message, name='chat_send'),
]
