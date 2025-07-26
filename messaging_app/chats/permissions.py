from rest_framework.permissions import BasePermission

class IsParticipantOfConversation(BasePermission):
    """
    Allows access only to authenticated users who are participants in the conversation.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Checks if the request user is a participant in the conversation
        conversation = getattr(obj, 'conversation', None)
        if not conversation:
            return False
        return request.user == conversation.sender or request.user == conversation.recipient