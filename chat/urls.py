from django.urls import path

from . import views

urlpatterns = [
    path("chat/", views.ChatRoomsHomeView.as_view(), name='chat'),
    path("chat/<str:room_name>/", views.RoomView.as_view(), name="room"),
]

