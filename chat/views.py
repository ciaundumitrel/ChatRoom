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

        conversations = Conversation.get_by_one_user(user=self.request.user)
        res = {}
        for friend in friends:
            for id_ in conversations:
                res[friend] = id_['id']
                conversations.remove(id_)
                break

        print(json.dumps(res))

        context['friends_conversation'] = (res)

        return context


class RoomView(LoginRequiredMixin, TemplateView):
    template_name = "pages/chat/room.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        conv = Conversation.get_by_pk(pk=kwargs['room_name'])

        messages = Message.objects.filter(conversation=conv).values('timestamp', 'text', 'sender')
        data = list(messages)
        context['messages'] = json.dumps(data, default=str)

        return context

    def dispatch(self, request, *args, **kwargs):
            return super(RoomView, self).dispatch(request, *args, **kwargs)
