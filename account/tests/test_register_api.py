from django.test import TestCase
from account.data_checker import check_register_data, check_register_name, check_register_email, check_register_password


class RegisterApiTest(TestCase):

    def test_register(self):
        # should be OK
        self.assertIsNone(
            check_register_data(
                {
                    "name": "Sam",
                    "email": "sam30718@gmail.com",
                    "password": "this_is_my_password"
                }
            )
        )

        # should be not OK
        self.assertIsNotNone(           # cannot empty
            check_register_data(
                {
                    "name": "",
                    "email": "",
                    "password": ""
                }
            )
        )

        self.assertIsNotNone(           # password too short
            check_register_data(
                {
                    "name": "查理布朗",
                    "email": "charlie@gmail.com",
                    "password": "short"
                }
            )
        )

        self.assertIsNotNone(            # password too long
            check_register_data(
                {
                    "name": "JOJO",
                    "email": "jojo@outlook.com",
                    "password": "1234567890123456789012345678901"
                }
            )
        )

        self.assertIsNotNone(           # name too long
            check_register_data(
                {
                    "name": "我的名字太長我的名字太長我的名字太長我的名字太長",
                    "email": "charlie@gmail.com",
                    "password": "short"
                }
            )
        )

        self.assertIsNotNone(           # email domain not support
            check_register_data(
                {
                    "name": "JOJO",
                    "email": "jojo@outlook.com",
                    "password": "short"
                }
            )
        )

    def test_register_name(self):
        # should be OK
        self.assertIsNone(check_register_name("Sam"))
        self.assertIsNone(check_register_name("我是何榮森"))
        self.assertIsNone(check_register_name("1"))
        self.assertIsNone(check_register_name("3.14159"))
        self.assertIsNone(check_register_name("-_+@, .\/`~!#$%^&*()"))
        self.assertIsNone(check_register_name("一二三四五六七八九十一二三四五六七八九十"))

        # should be not OK
        self.assertIsNotNone(check_register_name(""))
        self.assertIsNotNone(check_register_name("一二三四五六七八九十一二三四五六七八九十一"))

    def test_register_password(self):
        # should be OK
        self.assertIsNone(check_register_password("123456"))
        self.assertIsNone(check_register_password("my_password"))
        self.assertIsNone(check_register_password("!@#$%^&*()+{}[],./\s1"))

        # should be not OK
        self.assertIsNotNone(check_register_password(""))
        self.assertIsNotNone(check_register_password("1"))
        self.assertIsNotNone(check_register_password("12"))
        self.assertIsNotNone(check_register_password("123"))
        self.assertIsNotNone(check_register_password("1234"))
        self.assertIsNotNone(check_register_password("12345"))

    def test_register_email(self):
        # should be OK
        self.assertIsNone(check_register_email("test@gmail.com"))
        self.assertIsNone(check_register_email("test@hotmail.com"))
        self.assertIsNone(check_register_email("12345678901234567890123456789012345@gmail.com"))

        # should be not OK
        self.assertIsNotNone(check_register_email(""))
        self.assertIsNotNone(check_register_email("@"))
        self.assertIsNotNone(check_register_email("@gmail"))
        self.assertIsNotNone(check_register_email("@hotmail"))
        self.assertIsNotNone(check_register_email("@gmail.com"))
        self.assertIsNotNone(check_register_email("@hotmail.com"))
        self.assertIsNotNone(check_register_email("@hotmail.com"))
        self.assertIsNotNone(check_register_email("test@hotmail"))
        self.assertIsNotNone(check_register_email("test@gmail"))
        self.assertIsNotNone(check_register_email("123456789012345678901234567890123456@gmail.com"))

