import json
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, ListView
from accounts.models import Account
from feed.models import PostList, Comment
from friends.models import FriendRequest, FriendList
from convos.models import Conversation, Message


class HomePageView(LoginRequiredMixin, TemplateView):
    template_name = 'pages/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        login_user_id = self.request.user.id
        friend_requests = FriendRequest.objects.filter(receiver=login_user_id, is_active=True)
        data = []

        for fr in friend_requests:
            aux = [fr, fr.receiver, fr.timestamp]
            data.append(aux)

        context['friend_requests'] = data

        friends, _ = FriendList.objects.get_or_create(user=self.request.user)
        relevant_posts = []
        if friends.get_friends():
            friends_list = list(friends.get_friends())
            context['friends'] = friends_list
            for friend in friends_list:
                f = Account.objects.get(username=friend)
                posts, _ = PostList.objects.get_or_create(owner=f)
                if posts.posts.all():
                    this_posts = ([[f.username, f.profile_image, str(p.created), str(p.text), p.id,
                                    'liked' if p.id in list(posts.liked_posts.values_list('id', flat=True)) else '',
                                    'bookmarked' if p.id in list(
                                        posts.bookmarked_posts.values_list('id', flat=True)) else '',
                                    'reposted' if p.id in list(
                                        posts.reposted_posts.values_list('id', flat=True)) else '',
                                    [comment for comment in Comment.objects.filter(post=p)]]
                                   for p in posts.posts.all()])
                    for post in this_posts:
                        relevant_posts.append(post)

        posts, _ = PostList.objects.get_or_create(owner=self.request.user)

        if posts.posts.all():
            new_list = [
                [self.request.user.username, str(self.request.user.profile_image), str(p.created), str(p.text), p.id,
                 'liked' if p.id in list(posts.liked_posts.values_list('id', flat=True)) else '',
                 'bookmarked' if p.id in list(posts.bookmarked_posts.values_list('id', flat=True)) else '',
                 'reposted' if p.id in list(posts.reposted_posts.values_list('id', flat=True)) else '',
                 [comment.get_comment_data() for comment in Comment.objects.filter(post=p)]]
                for p in posts.posts.all()]
            for post in new_list:
                relevant_posts.append(post)

        relevant_posts.sort(key=lambda x: datetime.strptime(x[2], "%Y-%m-%d %H:%M:%S.%f%z"))
        context['posts'] = relevant_posts

        return context

    def post(self, request, *args, **kwargs):
        request_type = request.POST.dict()['request_type']
        if request_type == 'friend_request':
            request_data = request.POST.dict()['req_response']
            action, receiver, sender = request_data.split('-')
            sender_id = Account.objects.get(username=sender).id
            sender = Account.objects.get(username=sender)
            receiver_id = Account.objects.get(username=receiver).id
            receiver = Account.objects.get(username=receiver)
            friend_request = FriendRequest.objects.get(sender=sender_id, receiver=receiver_id)
            if friend_request:
                if 'accept' in action:
                    update_notification = friend_request.accept()
                    Conversation.objects.create(user1=receiver, user2=sender)
                    return HttpResponse('Accepted friend request')
                elif 'decline' in action:
                    update_notification = friend_request.decline()
                    return HttpResponse('Declined friend request request')
            else:
                return HttpResponse('Failes')
        else:
            return HttpResponse('123')


class AccountListView(ListView):
    model = Account
    template_name = 'pages/user_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        friends, _ = FriendList.objects.get_or_create(user=self.request.user)
        friends = list(friends.get_friends())
        users = list(Account.objects.values_list('username', flat=True))
        addable_users = list(set(users) - set(friends))

        context['addable_users'] = addable_users

        return context

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        data = json.load(request)
        request_data = data['request_from_to']
        r_from, r_to = request_data.split('-')
        user_from = Account.objects.get(username=r_from)
        user_to = Account.objects.get(username=r_to)
        friend_request, creation_date = FriendRequest.objects.get_or_create(
            sender=user_from,
            receiver=user_to,
        )
        friend_request.save()

        return HttpResponse('friend request got ok')
