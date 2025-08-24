import django_filters
from .models import Message

class MessageFilter(django_filters.FilterSet):
    created_at__gte = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    created_at__lte = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='lte')
    sender = django_filters.CharFilter(field_name='sender__username', lookup_expr='icontains')

    class Meta:
        model = Message
        fields = ['sender', 'created_at__gte', 'created_at__lte']