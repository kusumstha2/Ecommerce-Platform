from django.db import models
from  MainSystem.models import Notification
# Create your models here.
from django.db import models

from django.conf import settings
from django.contrib.auth import get_user_model
User = get_user_model()
class FCMTokens(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Use AUTH_USER_MODEL
    token = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.token}"


class NotificationToken(models.Model):
   owner = models.ForeignKey(User, on_delete = models.CASCADE)
   token = models.CharField(max_length=99999999, unique=True)
