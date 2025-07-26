from rest_framework import viewsets
from .models import Message
from .serializers import MessageSerializer
from .permissions import IsParticipantOfConversation

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsParticipantOfConversation]

    def get_queryset(self):
        user = self.request.user
        return Message.objects.filter(
            conversation__sender=user
        ) | Message.objects.filter(
            conversation__recipient=user
        )