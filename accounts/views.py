from django.shortcuts import redirect, render
from django.contrib import auth

from .forms import UserCreationForm
from .models import User

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
    if request.method == 'POST':
        email = request.POST.get('email', '') if 'email' in request.POST  else None
        password1 = request.POST.get('password', '') if 'password' in request.POST  else None
        password2 =  request.POST.get('confirm', '') if 'confirm' in request.POST  else None
        prenom = request.POST.get('prenom', '') if 'prenom' in request.POST else None
        nom = request.POST.get('nom', '') if 'nom' in request.POST else None
        data = {
            'email': email,
            'prenom': prenom,
            'nom': nom,
            'password1': password1,
            'password2': password2,
        }
        
        if User.objects.filter(email=email).first() is not None:
            return render(request, 'register.html',{"message": "Un utilisateur avec ce email exite déja"})

        user_form = UserCreationForm(data)
        if user_form.is_valid():
            print("user created")
            user_form.save()
            return redirect('login')
        else:
            return render(request, 'register.html',{"message": "Erreur:Veuillez revoir les informations soumisent"})
    else:
        return render(request, 'register.html')
