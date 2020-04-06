from django.test import TestCase, RequestFactory

from account.models import User
from account.apis import login
from board.apis import post

import json

name = 'Test'
email = 'test@gmail.com'
password = 'test_password'

token = ''


class PostApiTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # create user
        User.objects.create(name=name, email=email, password=password)

        # get token when login
        request = RequestFactory().post('/login/',
                                        data=json.dumps({'email': email, 'password': password}),
                                        content_type='application/json')
        global token
        token = json.loads(
            login(request=request).content
        )['token']

    def test_post_api(self):

        # post succeed
        response = json.loads(
            post(_get_request('/board/post/', {"content": '測試的發文哦'}, token=token)).content
        )['status']
        self.assertEqual('Post created', response)

        # post failed
        response = json.loads(
            post(_get_request('/board/post/', {"wrong_key": 'key設錯惹'}, token=token)).content
        )['status']
        self.assertNotEqual('Post created', response)


# #####################
#   Private methods
# #####################
def _get_request(path: str, body: dict, **headers):
    request = RequestFactory().post(path,
                                    data=json.dumps(body),
                                    content_type='application/json')
    new_headers = {'Cookie': '', 'Content-Length': '51', 'Content-Type': 'application/json'}

    for key, value in headers.items():
        new_headers[key] = value

    request.headers = new_headers
    return request
