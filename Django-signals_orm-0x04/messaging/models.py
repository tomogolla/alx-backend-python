
from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings

User = get_user_model()


class UnreadMessagesManager(models.Manager):
    def for_user(self, user):
        return self.get_queryset().filter(receiver=user, read=False).only('id', 'sender', 'content', 'timestamp')

class Message(models.Model):
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_messages'
    )
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_messages'
    )
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    parent_message = models.ForeignKey(
        'self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies'
    )
    read = models.BooleanField(default=False)
    
    objects = models.Manager()  # Default manager
    unread = UnreadMessagesManager() 
    def __str__(self):
        return f'{self.sender} -> {self.receiver}: {self.content[:20]}'

    def get_thread(self):
        """
        Recursively fetch all replies to this message.
        """
        thread = []

        def recurse(message):
            for reply in message.replies.all():
                thread.append(reply)
                recurse(reply)

        recurse(self)
        return thread


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.user}"


