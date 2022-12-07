from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings
from django.utils import timezone
# Create your models here.


class FriendList(models.Model):
    user = models.OneToOneField('accounts.Account', on_delete=models.CASCADE, related_name='user')
    friends = models.ManyToManyField('accounts.Account', blank=True, related_name='friends')

    def __str__(self):
        return self.user.username

    def add_friend(self, account):
        print('friends=', self.friends.all())
        if account not in self.friends.all():
            self.friends.add(account)
            self.save()

    def remove_friend(self, account):
        if account in self.friends.all():
            self.friends.remove(account)

    def unfriend(self, removable):
        remover_friends_list = self
        remover_friends_list.remove_friend(removable)
        friend_list = FriendList.objects.get(usr=removable)
        friend_list.remove_friend(self.user)

    def is_mutual_friend(self, friend):
        if friend in self.friends.all():
            return True
        else:
            return False

    def get_friends(self):
        return [str(friend) for friend in self.friends.all()]


class FriendRequest(models.Model):
    sender = models.ForeignKey('accounts.Account', on_delete=models.CASCADE, related_name="sender")
    receiver = models.ForeignKey('accounts.Account', on_delete=models.CASCADE, related_name="receiver")
    is_active = models.BooleanField(blank=False, null=False, default=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.sender.username

    def accept(self):
        """
        Accept friend request
        """
        receiver_friend_list, _ = FriendList.objects.get_or_create(user=self.receiver)
        print(receiver_friend_list)
        if receiver_friend_list:
            receiver_friend_list.add_friend(self.sender)
            sender_friend_list, _ = FriendList.objects.get_or_create(user=self.sender)
            if sender_friend_list:
                sender_friend_list.add_friend(self.receiver)
                self.is_active = False
                self.save()

    def decline(self):
        """
        Decline
        """
        self.is_active = False
        self.save()

    def cancel(self):
        self.is_active = False
        self.save()


