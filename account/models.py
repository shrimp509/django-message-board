from django.db import models
from django.utils import timezone


class User(models.Model):
    # filled by user
    name = models.fields.CharField(max_length=20)
    email = models.fields.EmailField(max_length=50)
    password = models.fields.CharField(max_length=30)

    # extra fields
    is_active = models.fields.BooleanField(default=True)
    is_admin = models.fields.BooleanField(default=False)
    last_login = models.fields.DateTimeField(null=True, blank=True)
    joined = models.fields.DateField(default=timezone.now)

    def username(self):
        return self.name

    def email(self):
        return self.email

    def password(self):
        return self.password

    def is_active(self):
        return self.is_active

    def is_admin(self):
        return self.is_admin

    def last_login(self):
        return self.last_login

    def joined(self):
        return self.last_login

    def __str__(self):
        return str(self.name) + "/" + str(self.email)


