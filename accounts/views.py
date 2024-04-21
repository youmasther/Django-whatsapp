from django.shortcuts import redirect, render
from django.contrib import auth

# Create your views here.

def login(request):
    user = request.user
    if user and user.is_authenticated:
        return redirect('chat')
    if request.POST:
        email = request.POST.get('email','') if 'email' in request.POST  else None
        password = request.POST.get('password', '') if 'password' in request.POST  else None
        user = auth.authenticate(email=email , password=password)
        if user and user.is_active:
            auth.login(request, user)
            return redirect('chat')
        else:
            return render(request, 'login.html', {'message': 'Login ou mot de passe incorrect'})
    else:
        return render(request, 'login.html', {'message': ''})

def register(request):
    return render(request, 'register.html')