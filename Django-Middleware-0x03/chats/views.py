from rest_framework import generics, permissions
from django_filters import rest_framework as filters
from .models import Message
from .serializers import MessageSerializer


# 🔍 Custom Filter Class for messages
class MessageFilter(filters.FilterSet):
    created_at__gte = filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    created_at__lte = filters.DateTimeFilter(field_name='created_at', lookup_expr='lte')

    class Meta:
        model = Message
        fields = ['sender', 'receiver', 'created_at__gte', 'created_at__lte']


# 📄 List + Create Messages View with pagination and filtering
class MessageListCreateView(generics.ListCreateAPIView):
    queryset = Message.objects.all().order_by('-created_at')
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]  # Adjust if you want anonymous access
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = MessageFilter
