from django.urls import path
from .views import login, register

urlpatterns = [
    path('', login, name="login"),
    path('register', register, name="register"),
]