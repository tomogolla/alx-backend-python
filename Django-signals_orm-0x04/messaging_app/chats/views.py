from rest_framework import viewsets, status, filters, permissions
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.shortcuts import render
from messaging.models import Message
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from django.contrib.auth import get_user_model
from .permissions import IsOwner, IsParticipantOfConversation
from rest_frameworks.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from .pagination import MessagePagination
from .filters import MessageFilter


User = get_user_model()


class ConversationViewSet(viewsets.ModelViewSet):
    """
    viewset for listing and creating conversations
    """
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated, IsParticipantOfConversation]
    filter_backends = [filters.SearchFilter]
    search_fields = ['participants_username']
    
    
    def perform_create(self, serializer):
        
        """ 
        automatically include the authenicated user as a participant
        """
        conversation = serializer.save()
        conversation.participants.add(self.request.user)
        conversation.save()
        
class MessageViewSet(viewsets.ModelViewSet):
    """ 
    viewsets for listings and creating messages within conversations
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated, IsParticipantOfConversation]
    pagination_class = MessagePagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = MessageFilter
    
    def perform_create(self, serializer):
        """ 
        set the sender to the current authenticated user
        """
        conversation_id = self.request.data.get('conversation')
        user = self.request.user

        try:
            conversation = Conversation.objects.get(id=conversation_id)
        except Conversation.DoesNotExist:
            return Response({'error': 'Conversation not found'}, status=status.HTTP_404_NOT_FOUND)

        # Check if user is part of the conversation
        if user not in conversation.participants.all():
            return Response({'error': 'You are not allowed to send messages to this conversation'},
                            status=status.HTTP_403_FORBIDDEN)

        serializer.save(sender=user, conversation=conversation)

class MessageListView(generics.ListAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, isOwner]
    
        
    def get_queryset(self)   :
        # only messages where the user is the sender or reciever
        user = self.request.user
        return Message.objects.filter(sender=user) | Message.objects.filter(reciever=user)
    
class ConversationListView(generics.ListAPIView):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    
    def get_queryset(self):
        return Conversation.objects.filter(sender=user) | Conversation.objects.filter(reciever=user)
    
    

@cache_page(60)
def conversation_view(request, conversation_id):
    messages = Message.objects.filter(conversation__id=conversation_id).select_related('sender', 'receiver')
    return render(request, 'chats/conversation.html', {
        'messages': messages
    })
