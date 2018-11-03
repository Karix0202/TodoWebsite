from django.db import models
from userauth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

class FriendRequest(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friends_request_sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friends_request_receibver')
    sended = models.DateField(auto_now_add=True)
    accepted = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.sender} | {self.receiver} at {self.sended}'
    
    class Meta:
        ordering = ('sended',)

@receiver(post_save, sender=FriendRequest)
def _user_save_friend_request(sender, instance, created, **kwargs):
    if not created:
        receiver = instance.receiver
        sender = instance.sender

        receiver.friends.add(sender)
        receiver.save()

        sender.friends.add(receiver)
        sender.save()

@receiver(post_delete, sender=FriendRequest)
def _post_delete_friend_request(sender, instance, **kwargs):
    if instance.accepted:
        receiver = instance.receiver
        sender = instance.sender

        receiver.friends.remove(sender)
        receiver.save()
        
        sender.friends.remove(receiver)
        sender.save()