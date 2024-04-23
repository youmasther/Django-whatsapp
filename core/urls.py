from django.urls import path
from .views import chat
from .hx_views import hx_chat, hx_create_message, hx_search

urlpatterns = [
    path('', chat, name="chat"),
    path('hx_chat/<int:id>', hx_chat, name="hx_chat"),
    path('hx_create_message', hx_create_message, name="hx_create_message"),
    path('hx_search', hx_search, name="hx_search"),
]