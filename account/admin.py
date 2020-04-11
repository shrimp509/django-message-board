from django.contrib import admin
from .models import User, BlackList

# Register your models here.
admin.site.register(User)
admin.site.register(BlackList)
