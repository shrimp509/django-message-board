from django.test import TestCase, RequestFactory

from account.models import User
from account.apis import login
from board.models import Post, Comment
from board.apis import t2_comment

import json

name = 'Test'
email = 'test@gmail.com'
password = 'test_password'

token = ''

post_id = 0
comment_id = 0


class T2CommentApiTest(TestCase):

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

        # create a comment
        comment = Comment()
        comment.post = post
        comment.author = user
        comment.content = "對測試發文留言哦"
        comment.save()

        # get comment_id
        for comment_item in Comment.objects.filter(content='對測試發文留言哦'):
            global comment_id
            comment_id = comment_item.id

    def test_t2comment_api(self):

        # POST /board/comment/{{comment_id}}/t2_comment/ succeed
        request = _get_request(
            '/board/comment/{}/t2_comment/'.format(comment_id),
            {"content": '這是測試的二階留言哦'},
            token=token
        )

        response = json.loads(
            t2_comment(request, comment_id).content
        )['status']
        self.assertEqual('T2Comment created', response)

        # POST /board/post/{{post_id}}/comment/ failed
        request = _get_request(
            '/board/comment/{}/t2_comment/'.format(comment_id),
            {"wrong_key": '這是測試的二階留言哦'},
            token=token
        )

        response = json.loads(
            t2_comment(request, comment_id).content
        )['status']
        self.assertNotEqual('T2Comment created', response)


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
