from django.core import serializers
from django.forms import model_to_dict
from django.http import HttpResponse
from django.shortcuts import render

from accounts.models import Account
from .models import Conversation, Message

import json
# Create your views here.


def get_conversation(request, *args, **kwargs):
    if request.method == 'POST':
        user1 = kwargs['user1']
        user2 = kwargs['user2']

        user1 = Account.objects.get(username=user1)
        user2 = Account.objects.get(username=user2)

        conv = Conversation.get(user1=user1, user2=user2)

        messages = Message.objects.filter(conversation=conv[0]).values('timestamp', 'text', 'sender')
        data = list(messages)

        return HttpResponse(json.dumps(data, default=str))

