from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from accounts.models import User
# Create your views here.

@login_required(login_url='/')
def chat(request):
    users = User.objects.exclude(email=request.user.email)
    context = {
        "users": users
    }
    return render(request, 'index.html', context)