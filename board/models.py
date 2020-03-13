from django.db import models
from django.utils import timezone


class Post(models.Model):
    content = models.TextField()
    created = models.fields.DateTimeField(default=timezone.now)
    publisher = models.fields.CharField(max_length=100)

    def __str__(self):
        return str(self.publisher) + ":" + str(self.content)


class Comment(models.Model):
    post_id = models.fields.CharField(max_length=100)
    content = models.fields.CharField(max_length=100)
    created = models.fields.DateTimeField(default=timezone.now)
    publisher = models.fields.CharField(max_length=100)

    def __str__(self):
        return str(self.publisher) + ":" + str(self.content)
