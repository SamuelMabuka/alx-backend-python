from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.status import HTTP_403_FORBIDDEN

from django_filters.rest_framework import DjangoFilterBackend

from .models import Message, Conversation
from .serializers import MessageSerializer
from .permissions import IsParticipantOfConversation
from .filters import MessageFilter  # ✅ Import the custom filter

class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    filter_backends = [DjangoFilterBackend]
    filterset_class = MessageFilter  # ✅ Add filtering

    def get_queryset(self):
        user = self.request.user
        return Message.objects.filter(
            conversation__sender=user
        ) | Message.objects.filter(
            conversation__recipient=user
        )

    def perform_create(self, serializer):
        conversation_id = self.request.data.get('conversation')
        try:
            conversation = Conversation.objects.get(id=conversation_id)
        except Conversation.DoesNotExist:
            raise PermissionDenied("Conversation not found")

        user = self.request.user
        if user != conversation.sender and user != conversation.recipient:
            raise PermissionDenied(
                detail="You are not a participant in this conversation.",
                code=HTTP_403_FORBIDDEN
            )

        serializer.save(sender=user, conversation=conversation)