from django.urls import path
from .views import RegisterPageView, ProfilePageView, EditProfilePageView

urlpatterns = [
    path('register/', RegisterPageView.as_view(), name='register'),
    path('profile/', ProfilePageView.as_view(), name='profile'),
    path('edit_profile/<int:pk>', EditProfilePageView.as_view(), name='edit_profile')
]
