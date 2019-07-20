from django.db import models


# Create your models here.
class App1(models.Model):
    name = models.CharField(max_length=255)
    ended = models.BooleanField(default=False)


class Paragraph(models.Model):
    app1 = models.ForeignKey(App1, on_delete=models.CASCADE)
    text = models.TextField()
    author = models.CharField(max_length=255)
