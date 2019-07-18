from django.db import models


# Create your models here.
class App1(models.Model):
    text = models.TextField()
    ended = models.BooleanField(default=False)