from django.shortcuts import render
from accounts.models import User, Messages
from django.db.models import Q

def hx_chat(request, id):
    id = id
    user = None
    messages = None
    if id : 
        user = User.objects.get(id=int(id))
    
    if user:
        messages = Messages.objects.filter(Q(sender=user, receiver=request.user) | Q(sender=request.user, receiver=user)).order_by('-timestamp')
    context = {
        "user": user,
        "messages" : messages
    }
    return render(request, 'hx_partials/hx_chat.html', context)