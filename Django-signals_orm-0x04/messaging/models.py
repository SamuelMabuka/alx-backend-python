from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from .managers import UnreadMessagesManager

class UnreadMessagesManager(models.Manager):
    def for_user(self, user):
        return self.get_queryset().filter(
            receiver=user,
            read=False
        ).select_related('sender').only('id', 'sender', 'content', 'timestamp')

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    parent_message = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)
    read = models.BooleanField(default=False)
    edited = models.BooleanField(default=False)
    edited_by = models.ForeignKey(  # <--- NEW FIELD
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='edited_messages'
    
    )
    
    parent_message = models.ForeignKey(
        'self',                  # reference Message itself
        null=True,               # root/top-level messages won't have a parent
        blank=True,
        on_delete=models.CASCADE,
        related_name='replies'   # makes it easy to get replies: message.replies.all()
    )
    objects = models.Manager()  # Default manager
    unread_messages = UnreadMessagesManager()  # Custom manager for unread messages
    
    def __str__(self):
        return f'Message from {self.sender.username} to {self.receiver.username}'


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)

    def __str__(self):
        return f'Notification for {self.user.username} - Message ID: {self.message.id}'


class MessageHistory(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='history')
    old_content = models.TextField()
    edited_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Edit history for message ID {self.message.id}'