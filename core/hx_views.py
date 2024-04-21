from django.shortcuts import render
from accounts.models import User

def hx_chat(request, id):
    id = id
    user = None
    if id : 
        user = User.objects.get(id=int(id))
    context = {
        "user": user
    }
    return render(request, 'hx_partials/hx_chat.html', context)