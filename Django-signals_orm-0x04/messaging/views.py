from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Message
from django.db.models import Prefetch

User = get_user_model()

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_user(request):
    user = request.user
    user.delete()  # Triggers the post_delete signal
    return Response({"message": "User deleted successfully."}, status=status.HTTP_200_OK)



@login_required
def user_conversations(request):
    messages = Message.objects.filter(
        sender=request.user
    ).select_related(
        'sender', 'receiver'
    ).prefetch_related(
        Prefetch('replies', queryset=Message.objects.select_related('sender', 'receiver'))
    )

    context = {
        'messages': messages
    }
    return render(request, 'messaging/conversations.html', context)


@login_required
def unread_messages_view(request):
    context = {
        'unread_messages': unread_messages
    }
    
    unread_messages = Message.unread.unread_for_user(request.user)
    return render(request, 'messaging/unread_messages.html', {
        'unread_messages': unread_messages
    })

