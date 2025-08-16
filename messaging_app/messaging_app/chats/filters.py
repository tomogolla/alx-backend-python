from django_filters import rest_framework as filters
from .models import Message

class MessageFilter(filters.FilterSet):
    start_date = filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    end_date = filters.DateTimeFilter(field_name='created_at', lookup_expr='lte')

    class Meta:
        model = Message
        fields = ['sender', 'conversation', 'start_date', 'end_date']