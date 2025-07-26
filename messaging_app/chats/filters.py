import django_filters
from .models import Message
from django.utils import timezone

class MessageFilter(django_filters.FilterSet):
    sender = django_filters.CharFilter(field_name='sender__username', lookup_expr='iexact')
    recipient = django_filters.CharFilter(field_name='conversation__recipient__username', lookup_expr='iexact')
    conversation = django_filters.NumberFilter(field_name='conversation__id')
    created_after = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    created_before = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='lte')

    class Meta:
        model = Message
        fields = ['sender', 'recipient', 'conversation', 'created_after', 'created_before']