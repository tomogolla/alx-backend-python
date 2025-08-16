from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from django.shortcuts import get_object_or_404
from .permissions import IsParticipantOfConversation
from django_filters.rest_framework import DjangoFilterBackend
from .filters import MessageFilter
from .pagination import CustomMessagePagination


class ConversationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows conversations to be viewed or created.
    """
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    
    def get_queryset(self):
        """Filters conversations to only those the user is a part of."""
        return self.request.user.conversations.all().prefetch_related('participants', 'messages')


class MessageViewSet(viewsets.ModelViewSet):
    """
    API endpoint for messages within a specific conversation.
    """
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    filter_backends = [DjangoFilterBackend]
    filterset_class = MessageFilter
    pagination_class = CustomMessagePagination

    def get_queryset(self):
        """
        This view returns a list of all messages for the conversation
        as determined by the conversation_id portion of the URL.
        """
        conversation_id = self.kwargs['conversation_id']
        conversation = get_object_or_404(Conversation, pk=conversation_id)

        if self.request.user not in conversation.participants.all():
            raise PermissionDenied(
                "You do not have permission to access this conversation.",
                code=status.HTTP_403_FORBIDDEN
            )
        
        return Message.objects.filter(conversation=conversation)

    def perform_create(self, serializer):
        """
        Associates the message with the conversation from the URL.
        """
        conversation_id = self.kwargs['conversation_id']
        conversation = get_object_or_404(Conversation, pk=conversation_id)
        self.check_object_permissions(self.request, conversation)
        serializer.save(sender=self.request.user, conversation=conversation)