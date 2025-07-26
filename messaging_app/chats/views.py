from rest_framework import viewsets, status, filters, permissions
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from django.contrib.auth import get_user_model
from .permissions import IsOwner



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
    
    
    def perform_create(self, serializer):
        """ 
        set the sender to the current authenticated user
        """
        serializer.save(sender = self.request.user)


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
    