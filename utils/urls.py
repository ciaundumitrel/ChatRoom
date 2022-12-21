from django.urls import path
from .views import SetReaction, SetComment

urlpatterns = [
   path('set_reaction/', SetReaction.as_view(), name='set_reaction'),
   path('set_comment/', SetComment.as_view(), name='set_comment')
   ]

