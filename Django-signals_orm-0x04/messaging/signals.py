
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Message, Notification
from .models import Message, MessageHistory



@receiver(post_save, sender=Message)
def create_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.receiver,
            message=instance
        )



@receiver(pre_save, sender=Message)
def log_message_edits(sender, instance, **kwargs):
    if not instance.pk:
        return  # It's a new message, no edits yet

    try:
        old_instance = Message.objects.get(pk=instance.pk)
    except Message.DoesNotExist:
        return

    if old_instance.content != instance.content:
        # Save old content
        MessageHistory.objects.create(
            message=old_instance,
            old_content=old_instance.content
        )
        instance.edited = True
