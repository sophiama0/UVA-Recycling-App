from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Message

@login_required
def inbox(request):
    # Show list of users the current user has chatted with
    users = User.objects.exclude(id=request.user.id)
    return render(request, 'messaging/inbox.html', {'users': users, 'messages_active': 'active'})

@login_required
def chat(request, username):
    other_user = User.objects.get(username=username)
    messages = Message.objects.filter(
        sender__in=[request.user, other_user],
        receiver__in=[request.user, other_user]
    ).order_by('timestamp')

    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Message.objects.create(sender=request.user, receiver=other_user, content=content)
            return redirect('messaging:chat', username=other_user.username)

    return render(request, 'messaging/chat.html', {'other_user': other_user, 'chat_messages': messages, 'messages_active': 'active'})
