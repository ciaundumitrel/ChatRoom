from django.http import JsonResponse, HttpResponse
from django.views import View

from feed.models import Post, PostList, Comment


class SetReaction(View):
    def dispatch(self, request, *args, **kwargs):
        post_id = request.GET['id']
        action = request.GET['action']
        post_owner = PostList.objects.all().get(owner=self.request.user)
        if action == '1':
            post_owner.add_liked_post(Post.objects.all().get(id=post_id))
        elif action == '3':
            post_owner.add_reposted_post(Post.objects.all().get(id=post_id))
        elif action == '4':
            post_owner.add_bookmarked_post(Post.objects.all().get(id=post_id))

        return JsonResponse(({'id': post_id, 'action': action}), safe=False)


class SetComment(View):
    def dispatch(self, request, *args, **kwargs):
        post_id = self.request.GET['id']
        post = Post.objects.get(id=post_id)
        text = self.request.GET['text']
        comment = Comment(text=text, user=self.request.user, post=post)
        comment.save()
        return JsonResponse({'1': 2})


