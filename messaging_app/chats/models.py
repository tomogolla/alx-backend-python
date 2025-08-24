from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

class User(AbstractUser):
    """
    Extended User model that inherits from Django's AbstractUser.
    Adds additional fields required by the application.
    """
    ROLE_CHOICES = [
        ('guest', 'Guest'),
        ('host', 'Host'),
        ('admin', 'Admin'),
    ]
    
    user_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        db_index=True
    )
    first_name = models.CharField(max_length=150, null=False, blank=False)
    last_name = models.CharField(max_length=150, null=False, blank=False)
    email = models.EmailField(unique=True, null=False, blank=False)
    
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        null=False,
        blank=False,
        default='guest'
    )
    
    # Django's AbstractUser already provides:
    # - password field (handled by Django's auth system)
    # - date_joined (equivalent to created_at)
    class Meta:
        db_table = 'auth_user'  # Keep Django's default user table name
        indexes = [
            models.Index(fields=['email']),  # Additional index on email
        ]
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"


class Conversation(models.Model):
    """
    Model to track conversations between users.
    Uses a many-to-many relationship to handle multiple participants.
    """
    conversation_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        db_index=True
    )
    
    participants = models.ManyToManyField(
        User,
        related_name='conversations',
        blank=False
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'conversation'
        indexes = [
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        participant_names = ', '.join([
            f"{user.first_name} {user.last_name}" 
            for user in self.participants.all()[:3]
        ])
        if self.participants.count() > 3:
            participant_names += f" and {self.participants.count() - 3} others"
        return f"Conversation: {participant_names}"


class Message(models.Model):
    """
    Model to store individual messages within conversations.
    """
    message_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        db_index=True
    )
    
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sent_messages',
        null=False
    )
    
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name='messages',
        null=False
    )
    
    message_body = models.TextField(null=False, blank=False)
    
    sent_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'message'
        indexes = [
            models.Index(fields=['sender']),
            models.Index(fields=['conversation']),
            models.Index(fields=['sent_at']),
            models.Index(fields=['conversation', 'sent_at']),  # Compound index for efficient message retrieval
        ]
        ordering = ['sent_at']  # Default ordering by timestamp
    
    def __str__(self):
        return f"Message from {self.sender.first_name} at {self.sent_at.strftime('%Y-%m-%d %H:%M')}"
    
    def clean(self):
        """
        Custom validation to ensure sender is a participant in the conversation.
        """
        from django.core.exceptions import ValidationError
        
        if self.conversation and self.sender:
            if not self.conversation.participants.filter(id=self.sender.id).exists():
                raise ValidationError(
                    "Sender must be a participant in the conversation."
                )


# Additional utility methods that might be helpful
class ConversationManager(models.Manager):
    """
    Custom manager for Conversation model with useful query methods.
    """
    def get_user_conversations(self, user):
        """Get all conversations for a specific user."""
        return self.filter(participants=user)
    
    def get_conversation_between_users(self, user1, user2):
        """Get conversation between two specific users (if exists)."""
        return self.filter(
            participants=user1
        ).filter(
            participants=user2
        ).filter(
            participants__count=2
        ).first()


# Add the custom manager to Conversation model
Conversation.add_to_class('objects', ConversationManager())


class MessageManager(models.Manager):
    """
    Custom manager for Message model with useful query methods.
    """
    def get_conversation_messages(self, conversation):
        """Get all messages for a specific conversation, ordered by timestamp."""
        return self.filter(conversation=conversation).order_by('sent_at')
    
    def get_user_messages(self, user):
        """Get all messages sent by a specific user."""
        return self.filter(sender=user)


# Add the custom manager to Message model  
Message.add_to_class('objects', MessageManager())