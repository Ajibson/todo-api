from django.db import models
from account.models import Account

class Todo(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    completed = models.BooleanField(default=False)
    to_be_deleted_at = models.DateTimeField(blank=True, null=True)
    starred = models.BooleanField(default=False)

    def __str__(self):
        return self.title
