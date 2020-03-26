from django.db import models
from django.utils import timezone


class User(models.Model):
    # required fields in First Registration page
    first_name = models.fields.CharField(max_length=20)
    last_name = models.fields.CharField(max_length=20)
    email = models.fields.EmailField(max_length=50)
    birthday = models.fields.DateField()
    gender = models.fields.CharField(max_length=10)
    phone = models.fields.CharField(max_length=10)

    # required fields in Second Registration page
    account = models.fields.CharField(max_length=30)
    password = models.fields.CharField(max_length=30)

    # extra fields
    is_staff = models.fields.BooleanField(default=False)
    is_active = models.fields.BooleanField(default=True)
    is_admin = models.fields.BooleanField(default=False)
    last_login = models.fields.DateTimeField(null=True, blank=True)
    date_joined = models.fields.DateField(default=timezone.now)

    def get_username(self):
        return self.name

    def get_account(self):
        return self.account

    def get_email(self):
        return self.email

    def __str__(self):
        return str(self.first_name) + " " + str(self.last_name)


