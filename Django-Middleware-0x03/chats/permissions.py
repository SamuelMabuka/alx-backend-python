from rest_framework.permissions import BasePermission
from rest_framework import exceptions

class IsParticipantOfConversation(BasePermission):
    """
    Custom permission to allow only authenticated participants of a conversation to interact with messages.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        conversation = getattr(obj, 'conversation', None)
        if not conversation:
            return False

        user = request.user
        is_participant = user == conversation.sender or user == conversation.recipient

        # Restrict unsafe methods to participants only
        if request.method in ['GET', 'PUT', 'PATCH', 'DELETE']:
            return is_participant

        return True  # Allow POST if authenticated (validated in view)