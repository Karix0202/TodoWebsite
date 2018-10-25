from django.db import models
from userauth.models import User

class FriendRequest(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friends_request_sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friends_request_receibver')
    sended = models.DateField(auto_now_add=True)
    accepted = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.sender} | {self.receiver} at {self.sended}'
    
    class Meta:
        ordering = ('sended',)