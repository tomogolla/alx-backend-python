from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from django.utils import timezone
from django.conf import settings


class User(AbstractUser):
    user_id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    is_online = models.BooleanField(default=False)
    last_seen = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateField(auto_now=True)
    password = models.CharField(max_length=128) # explicitly asked to define.

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email", "first_name", "last_name"]

    class Meta:
        ordering = ['username']
        verbose_name = 'Chat user'
        db_table = 'users'

    def __str__(self):
        return f"{self.get_full_name()} - {self.email}"


class Conversation(models.Model):
    conversation_id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    name = models.CharField(max_length=100, blank=True, null=True)
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='conversations')
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Chat Conversation'
        db_table = 'conversations'

    def __str__(self):
        usernames = " - ".join([user.username for user in self.participants.all()])
        return self.name if self.name else f"{usernames} Chat"


class Message(models.Model):
    message_id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_messages')
    message_body = models.TextField()
    sent_at = models.DateField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-sent_at']
        verbose_name = 'Chat Message'
        db_table = 'messages'

    def __str__(self):
        return f"{self.sender.username}: {self.message_body[:50]}..."
