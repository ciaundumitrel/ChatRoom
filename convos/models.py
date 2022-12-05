from django.db import models
from django.conf import settings
from django.db.models import DO_NOTHING
from django.utils import timezone

# Create your models here.


class Conversation(models.Model):
    user1 = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, default='1', related_name='user1')
    user2 = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, default='1', related_name='user2')

    # def add_message(self, message, timestamp):
    #     print(self.messages)
    #     self.messages.append((message, timestamp))
    #
    # def get_all_messages(self):
    #     print(self.messages)
    #     return self.messages
    #
    # def get_range_messages(self, n, m):
    #     return self.messages[n: m]

    def __str__(self):
        return "{}-{} ".format(str(self.user1), str(self.user2))


    @classmethod
    def get(cls, user1, user2):
        """ Gets all conversations between userA and userB
        """

        if user1.id > user2.id:
            (user1, user2) = (user2, user1)

        return cls.objects.filter(user1=user1, user2=user2)


class Message(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    text = models.CharField(max_length=100)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, null=True)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=DO_NOTHING, default='1')

    def save(self, *args, **kwargs):
        self.timestamp = timezone.now()
        # self.conversation.add_message(self.text, self.timestamp)

        super(Message, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.text)

