from django.db import models


class PostList(models.Model):
    owner = models.OneToOneField('accounts.Account', on_delete=models.CASCADE, related_name='post_owner')
    posts = models.ManyToManyField('feed.Post', null=True, related_name='post_list')
    liked_posts = models.ManyToManyField('feed.Post', null=True, related_name='liked_posts')
    reposted_posts = models.ManyToManyField('feed.Post', null=True, related_name='reposted_posts')
    bookmarked_posts = models.ManyToManyField('feed.Post', null=True, related_name='bookmarked_posts')

    def add_liked_post(self, post):
        if post not in self.liked_posts.all():
            self.liked_posts.add(post)
        else:
            self.liked_posts.remove(post)

    def add_bookmarked_post(self, post):
        if post not in self.bookmarked_posts.all():
            self.bookmarked_posts.add(post)
        else:
            self.bookmarked_posts.remove(post)

    def add_reposted_post(self, post):
        if post not in self.reposted_posts.all():
            self.reposted_posts.add(post)
        else:
            self.reposted_posts.remove(post)


class Post(models.Model):
    created = models.DateTimeField(auto_now=True)
    text = models.TextField()

    def __str__(self):
        return self.text


class Comment(models.Model):
    text = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey('accounts.Account', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_comment_data(self):
        return [
            self.text,
            self.user.profile_image,
            self.user.username,
            self.created_at.strftime("%d %b, %Y %H %M %S %p")
        ]
