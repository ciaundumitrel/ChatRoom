from django.urls import path

from .views import get_conversation

urlpatterns = [
    path('get_messages/<str:user1>-<str:user2>', get_conversation, name='get_conversation')
]
