from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Message


@login_required
def inbox(request):
    users = User.objects.exclude(id=request.user.id)
    user_chats = []

    for user in users:
        last_message = Message.objects.filter(
            Q(sender=request.user, receiver=user) | Q(sender=user, receiver=request.user)
        ).order_by('-timestamp').first()

        user_chats.append(
            {
                'user': user,
                'last_message': last_message.content if last_message else '',
                'last_timestamp': last_message.timestamp if last_message else None
            }
        )

    return render(request, 'messaging/inbox.html', {'user_chats': user_chats, 'messages_active': 'active'})


@login_required
def chat(request, first_name, user_id):
    other_user = User.objects.get(id=user_id)
    messages = Message.objects.filter(
        sender__in=[request.user, other_user],
        receiver__in=[request.user, other_user]
    ).order_by('timestamp')

    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Message.objects.create(sender=request.user, receiver=other_user, content=content)
            return redirect('messaging:chat', first_name=other_user.first_name, user_id=other_user.id)

    return render(request, 'messaging/chat.html', {'other_user': other_user, 'chat_messages': messages, 'messages_active': 'active'})


@login_required
def chat_messages_api(request, first_name, user_id):
    other_user = User.objects.get(id=user_id)

    messages = Message.objects.filter(
        sender__in=[request.user, other_user],
        receiver__in=[request.user, other_user]
    ).order_by('timestamp')

    data = [
        {
            'sender_id': msg.sender.id,
            'sender_first_name': msg.sender.first_name or msg.sender.username,
            'content': msg.content,
            'timestamp': msg.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        }
        for msg in messages
    ]

    return JsonResponse({'messages': data})