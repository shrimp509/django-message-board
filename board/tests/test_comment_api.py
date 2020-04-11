from django.test import TestCase, RequestFactory

from account.models import User
from account.apis import login
from board.models import Post
from board.apis import comment

import json

name = 'Test'
email = 'test@gmail.com'
password = 'test_password'

token = ''

post_id = 0


class CommentApiTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # create user
        user = User.objects.create(name=name, email=email, password=password)

        # get token when login
        request = RequestFactory().post('/login/',
                                        data=json.dumps({'email': email, 'password': password}),
                                        content_type='application/json')
        global token
        token = json.loads(
            login(request=request).content
        )['token']

        # create a post
        post = Post()
        post.author = user
        post.content = "測試用的發文"
        post.save()

        # get post_id
        for post_item in Post.objects.filter(content="測試用的發文"):
            global post_id
            post_id = post_item.id

    def test_comment_api(self):

        # POST /board/post/{{post_id}}/comment/ succeed
        request = _get_request(
            '/board/post/{}/comment/'.format(post_id),
            {"content": '我要對發文做測試的留言囉'},
            Authorization=token
        )

        response = json.loads(
            comment(request, post_id).content
        )['status']
        self.assertEqual('Comment created', response)

        # POST /board/post/{{post_id}}/comment/ failed
        request = _get_request(
            '/board/post/{}/comment/'.format(post_id),
            {"wrong_key": '我要對發文做測試的留言囉'},
            Authorization=token
        )

        response = json.loads(
            comment(request, post_id).content
        )['status']
        self.assertNotEqual('Comment created', response)


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
