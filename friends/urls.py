from django.urls import path
from .views import friend_request

urlpatterns = [
    path('send_friend_request/', friend_request, name='sent_friend_request'),
    ]
