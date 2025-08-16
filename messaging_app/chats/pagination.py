from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class CustomMessagePagination(PageNumberPagination):
    """
    Custom pagination class for messages to include total count and other details.
    """
    page_size = 20  # Number of messages per page
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        """
        Overrides the default paginated response to add the total count.
        """
        return Response({
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'count': self.page.paginator.count,
            'results': data
        })