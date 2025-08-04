import django_filters
from .models import Message

class MessageFilter(django_filters.FilterSet):
    start_date = django_filters.DateTimeFilter(field_name="timestamp", lookup_expr='gte')
    end_date = django_filters.DateTimeFilter(field_name="timestamp", lookup_expr='lte')
    sender = django_filters.CharFilter(field_name="sender__email", lookup_expr='icontains')
    conversation = django_filters.CharFilter(field_name="conversation__id")

    class Meta:
        model = Message
        fields = ['sender', 'conversation', 'start_date', 'end_date']
