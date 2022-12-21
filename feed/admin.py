from django.contrib import admin
from feed.models import Post, PostList, Comment


# Register your models here.


class PostsAmin(admin.ModelAdmin):
    list_display = ['text', 'created']

    class Meta:
        model = Post



class PostsListAmin(admin.ModelAdmin):
    list_display = ['owner']

    class Meta:
        model = PostList


admin.site.register(Post, PostsAmin)
admin.site.register(PostList, PostsListAmin)
admin.site.register(Comment)
