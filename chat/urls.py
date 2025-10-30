from django.urls import path
from . import views

urlpatterns = [
    path('<int:booking_id>/', views.chat_room, name='chat_room'),
    path('<int:booking_id>/messages/', views.get_chat_messages, name='get_chat_messages'),
]