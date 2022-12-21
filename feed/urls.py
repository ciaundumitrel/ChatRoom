from django.urls import path
from feed.views import create_post
urlpatterns = [
    path('creation_post/', create_post, name='create_post')
]
