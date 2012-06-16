from django.db import models
from players.models import UserProfile

class Message(models.Model):

    user = models.ForeignKey(UserProfile)
    timestamp = models.DateTimeField(auto_now_add=True)
    message = models.CharField(max_length=140)