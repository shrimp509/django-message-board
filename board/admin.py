from django.contrib import admin
from .models import Post, Comment, T2Comment

# Register your models here.
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(T2Comment)
