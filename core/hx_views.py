from django.shortcuts import render
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt

from accounts.models import User, Messages
from accounts.forms import MessagesCreationForm

def hx_chat(request, id):
    id = id
    user = None
    messages = None
    if id : 
        user = User.objects.get(id=int(id))
    
    if user:
        messages = Messages.objects.filter(Q(sender=user, receiver=request.user) | Q(sender=request.user, receiver=user)).order_by('timestamp')
    context = {
        "user": user,
        "messages" : messages
    }
    return render(request, 'hx_partials/hx_chat.html', context)

def hx_create_message(request):
    if request.method == "POST":
        id = request.POST['id'] if 'id' in request.POST  else None
        content = request.POST['content'] if 'content' in request.POST  else None
        data = {
            "sender": request.user,
            "receiver": User.objects.get(id=int(id)),
            "content": content,
            "media_url": None
        }
        form = MessagesCreationForm(data=data)
        new_message = None
        if form.is_valid():
            new_message = form.save()
        context =  {"message": new_message}
        return render(request, 'hx_partials/hx_chat_message.html', context)

@csrf_exempt
def hx_search(request):
    if request.method == "POST":
        search_query = request.POST["search"]
        users = User.objects.filter(Q(prenom__icontains=search_query)|Q(nom__icontains=search_query)).exclude(email=request.user.email)
        context={
            "users": users
        }

        return render(request, 'hx_partials/hx_side_bar_search.html', context)