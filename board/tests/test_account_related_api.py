from django.test import TestCase
from account.data_checker import find_user

from account.models import User

name = 'Test'
email = 'test@gmail.com'
password = 'test_password'


class UserTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        User.objects.create(name=name, email=email, password=password)

    def test_find_user(self):
        # correct
        self.assertIsInstance(find_user(email), User)

        # wrong
        self.assertIsInstance(find_user('wrong@gmail.com'), str)
