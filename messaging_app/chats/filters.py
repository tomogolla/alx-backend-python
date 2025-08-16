import django_filters
from .models import Message

class MessageFilter(django_filters.FilterSet):
    """
    FilterSet for querying Messages by sender and time range.
    """
    # Filter by the sender's email
    sender_email = django_filters.CharFilter(field_name='sender__email', lookup_expr='icontains')

    # Filter messages sent after a certain datetime
    start_date = django_filters.DateTimeFilter(field_name="sent_at", lookup_expr='gte')

    # Filter messages sent before a certain datetime
    end_date = django_filters.DateTimeFilter(field_name="sent_at", lookup_expr='lte')

    class Meta:
        model = Message
        fields = ['sender_email', 'start_date', 'end_date']