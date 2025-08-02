from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Message, Notification

@receiver(post_save, sender=Message)
def create_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.receiver,
            message=instance
        )

@receiver(pre_save, sender=Message)
def save_message_edit_history(sender, instance, **kwargs):
    if instance.pk:
        try:
            original = Message.objects.get(pk=instance.pk)
            if original.content != instance.content:
                # Mark message as edited
                instance.edited = True
                # Save old version to history
                MessageHistory.objects.create(
                    message=original,
                    old_content=original.content
                )
        except Message.DoesNotExist:
            pass  # Safe guard for race conditions