from django.test import TestCase
from account.data_checker import check_login_data, check_email_the_same, check_password_the_same

from account.models import User

name = 'Test'
email = 'test@gmail.com'
password = 'test_password'


class LoginApiTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        User.objects.create(name=name, email=email, password=password)

    def test_login(self):
        # should be OK
        self.assertIsNone(
            check_login_data(
                {
                    "email": email,
                    "password": password
                }
            )
        )

        # should be not OK
        self.assertIsNotNone(                           # empty info
            check_login_data(
                {
                    "email": "",
                    "password": ""
                }
            )
        )

        self.assertIsNotNone(
            check_login_data(
                {
                    "email": "test@hotmail.com",        # wrong email
                    "password": password
                }
            )
        )

        self.assertIsNotNone(
            check_login_data(
                {
                    "email": email,
                    "password": "password"              # wrong password
                }
            )
        )

    def test_login_email_the_same(self):
        users = User.objects.filter(email=email)

        # should be 1 exactly same user
        self.assertEqual(1, len(users))

        # should be OK
        for user in users:
            self.assertIsNone(
                check_email_the_same(email, user.email)
            )

        # should be not OK
        self.assertIsNotNone(
            check_email_the_same(email, "test@hotmail.com")
        )

        self.assertIsNotNone(
            check_email_the_same(email, "test123@gmail.com")
        )

    def test_login_password_the_same(self):
        users = User.objects.filter(email=email)

        # should be 1 exact same user
        self.assertEqual(1, len(users))

        # should be OK
        for user in users:
            self.assertIsNone(
                check_password_the_same(password, user.password)
            )

        # should be not OK
        self.assertIsNotNone(
            check_password_the_same(password, "password")
        )

        self.assertIsNotNone(
            check_password_the_same(password, "test")
        )

        self.assertIsNotNone(
            check_password_the_same(password, "123456")
        )
