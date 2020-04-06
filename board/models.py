from django.db import models
from django.utils import timezone

from account.models import User


class Post(models.Model):
    # related to User
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    # attributes
    content = models.fields.TextField(blank=True)
    liked = models.fields.PositiveIntegerField(default=0)

    created = models.fields.DateTimeField(default=timezone.now)
    last_updated = models.fields.DateTimeField(default=timezone.now)

    def edit(self, content):
        self.content = content
        self.last_updated = timezone.now

    def __unicode__(self):
        if len(str(self.content)) > 10:
            return str(self.author) + ":" + str(self.content)[0:10]
        else:
            return str(self.author) + ":" + str(self.content)

    def __str__(self):
        return str(self.author) + ":" + str(self.content)


class Comment(models.Model):
    # related to User
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    # related to Post
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    # attributes
    content = models.fields.CharField(max_length=100)
    liked = models.fields.PositiveIntegerField(default=0)

    created = models.fields.DateTimeField(default=timezone.now)
    last_updated = models.fields.DateTimeField(default=timezone.now)

    def edit(self, content):
        self.content = content
        self.last_updated = timezone.now

    def __unicode__(self):
        if len(str(self.content)) > 10:
            return str(self.author) + ":" + str(self.content)[0:10]
        else:
            return str(self.author) + ":" + str(self.content)

    def __str__(self):
        return str(self.author) + ":" + str(self.content)


class T2Comment(models.Model):
    # related to User
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    # related to Comment
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)

    # attributes
    content = models.fields.CharField(max_length=100)
    liked = models.fields.PositiveIntegerField(default=0)

    created = models.fields.DateTimeField(default=timezone.now)
    last_updated = models.fields.DateTimeField(default=timezone.now)

    def edit(self, content):
        self.content = content
        self.last_updated = timezone.now

    def __unicode__(self):
        if len(str(self.content)) > 10:
            return str(self.author) + ":" + str(self.content)[0:10]
        else:
            return str(self.author) + ":" + str(self.content)

    def __str__(self):
        return str(self.author) + ":" + str(self.content)