from django.urls import path
from .views import chat
from .hx_views import hx_chat

urlpatterns = [
    path('', chat, name="chat"),
    path('hx_chat/<int:id>', hx_chat, name="hx_chat"),
]