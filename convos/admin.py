from django.contrib import admin

from convos.models import Conversation, Message

# Register your models here.


class ConversationAdmin(admin.ModelAdmin):
    list_filter = ['user1', 'user2']

    class Meta:
        model = Conversation


class MessageAdmin(admin.ModelAdmin):
    list_display = ['text']


admin.site.register(Conversation, ConversationAdmin)
admin.site.register(Message, MessageAdmin)
