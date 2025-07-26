from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from .models import Message, Conversation
from .serializers import MessageSerializer
from .permissions import IsParticipantOfConversation
from .filters import MessageFilter
from .pagination import MessagePagination  # ✅ import custom paginator

class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    filter_backends = [DjangoFilterBackend]
    filterset_class = MessageFilter
    pagination_class = MessagePagination  # ✅ enable pagination

    def get_queryset(self):
        user = self.request.user
        return Message.objects.filter(
            conversation__sender=user
        ) | Message.objects.filter(
            conversation__recipient=user
        )

    def perform_create(self, serializer):
        conversation_id = self.request.data.get('conversation')
        conversation = Conversation.objects.get(id=conversation_id)
        if self.request.user != conversation.sender and self.request.user != conversation.recipient:
            raise PermissionDenied("Not a participant")
        serializer.save(sender=self.request.user, conversation=conversation)