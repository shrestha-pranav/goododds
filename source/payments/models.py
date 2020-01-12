from django.db import models
from django.contrib.auth.models import User

class Credits(models.Model):
    user        = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at  = models.DateTimeField(auto_now_add=True)
    num_credits = models.BigIntegerField()
