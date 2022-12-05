# chat/views.py
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import TemplateView

from accounts.models import Account
from convos.models import Conversation, Message
from friends.models import FriendList

import json

class ChatRoomsHomeView(LoginRequiredMixin, TemplateView):
    template_name = "pages/chat/index.html"

    def get_context_data(self, **kwargs):
        context = super(ChatRoomsHomeView, self).get_context_data()

        friends, _ = FriendList.objects.get_or_create(user=self.request.user)
        if friends.get_friends():
            friends = list(friends.get_friends())

        print(friends)
        context['friends'] = friends

        return context


class RoomView(LoginRequiredMixin, TemplateView):
    template_name = "pages/chat/room.html"

    def get_context_data(self, **kwargs):
        print(kwargs)
        context = super(RoomView, self).get_context_data()
        context['room_name'] = kwargs['room_name']
        user1, user2 = kwargs['room_name'].split('_')

        user1 = Account.objects.get(username=user1)
        user2 = Account.objects.get(username=user2)

        print(user1, user2)
        conv = Conversation.get(user1=user1, user2=user2)

        messages = Message.objects.filter(conversation=conv[0]).values('timestamp', 'text', 'sender')
        data = list(messages)
        context['messages'] = json.dumps(data, default=str)

        return context


    def dispatch(self, request, *args, **kwargs):
            return super(RoomView, self).dispatch(request, *args, **kwargs)
