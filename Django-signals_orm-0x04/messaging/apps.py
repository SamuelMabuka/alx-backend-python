from django.apps import AppConfig
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Message, Notification
from django.apps import AppConfig

class MessagingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'messaging'


@receiver(post_save, sender=Message)
def create_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.receiver,
            message=instance
        )

def ready(self):
    import messaging.signals  # Ensure signals are imported when the app is ready