import datetime

from django.http import HttpResponse
from django.shortcuts import render
from django.apps import apps
import json

def create_post(request):

    text = request.POST['text']
    sender = request.POST['sender']

    post = apps.get_model('feed.Post')
    post_list = apps.get_model('feed.PostList')
    account = apps.get_model('accounts.Account')
    account = account.objects.get(username=sender)

    post_obj = post(text=text, created=datetime.datetime.now())
    post_obj.save()

    postlist, _ = post_list.objects.get_or_create(owner=account)
    postlist.posts.add(post_obj)

    return HttpResponse('Got data')
