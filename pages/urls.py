from django.urls import path
from .views import HomePageView, AccountListView

urlpatterns = [
   path('home/', HomePageView.as_view(), name='home'),
   path('friend_search/', AccountListView.as_view(), name='friend_search'),

   ]
