from django.db import models
from django.conf import settings
from django.utils import timezone

# Create your models here.


class Conversation(models.Model):
    user1 = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.CASCADE,
                              blank=True, default='1',
                              related_name='user1')

    user2 = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.CASCADE,
                              blank=True, default='1',
                              related_name='user2')

    def __str__(self):
        return "{}-{} ".format(str(self.user1), str(self.user2))

    @classmethod
    def get_by_pk(cls, pk):
        return cls.objects.get(id=pk)

    @classmethod
    def get(cls, user1, user2):
        """ Gets all conversations between userA and userB
        """

        if user1.id > user2.id:
            (user1, user2) = (user2, user1)

        return cls.objects.filter(user1=user1, user2=user2)

    @classmethod
    def get_by_one_user(cls, user):
        conversations = list(cls.objects.filter(user1=user).values('id'))
        conversations += list(cls.objects.filter(user2=user).values('id'))
        return conversations


class Message(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    text = models.CharField(max_length=100)
    conversation = models.ForeignKey('convos.Conversation', on_delete=models.CASCADE, null=True)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, default='1')

    def save(self, *args, **kwargs):
        self.timestamp = timezone.now()
        super(Message, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.text)

