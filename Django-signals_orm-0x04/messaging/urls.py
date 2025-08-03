# messaging/urls.py
from django.urls import path
from .views import delete_user

urlpatterns = [
    path('delete/', delete_user, name='delete_user'),
]
