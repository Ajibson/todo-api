from django.contrib.auth.models import AbstractUser
from django.db import models


class Account(AbstractUser):
    pass

    def __str__(self):
        return self.username


class Token(models.Model):
    refresh_token = models.TextField()
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_blacklisted = models.BooleanField(default=False)
    blacklisted_at = models.DateTimeField(auto_now=True)    

    def __str__(self):
        return self.refresh_token