import jwt
import json
import datetime

from django.core.handlers.wsgi import WSGIRequest
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from message_board.settings import SECRET_KEY

from .models import Post, Comment
from account.data_checker import find_user
from account.models import User


# #####################
#   APIs
# #####################
@csrf_exempt
def post(request: WSGIRequest):
    if request.method == 'GET':
        all_posts = _get_all_posts()
        return _return_status('Get posts succeed', posts=all_posts)
    elif request.method == 'POST':

        token_body = _resolve_jwt(request.headers.get('token'))

        if type(token_body) is TokenBody:
            # valid token
            request_body = _resolve_request_body(request)
            try:
                if _save_post(request_body, token_body):
                    return _return_status('Post created')
                else:
                    return _return_status('Failed to create Post')
            except KeyError as e:
                return _return_status('Wrong request body format', err_msg='body should be `content`')
        else:
            # invalid token
            return _return_status('Invalid token', err_msg='token invalid or expired')
    else:
        return _return_status('No such method')


# #####################
#   Custom Class
# #####################
class TokenBody:
    # attributes
    email: str = ""
    password: str = ""

    def __init__(self, decoded_token_body):
        try:
            self.email = decoded_token_body['email']
            self.password = decoded_token_body['password']
        except Exception as e:
            raise e


# #####################
#   Private methods
# #####################
def _return_status(status: str, **kwargs):
    msg = {'status': status}
    for key, value in kwargs.items():
        msg[key] = value
    return JsonResponse(msg)


def _resolve_jwt(token):
    try:
        data = jwt.decode(token, SECRET_KEY)
        return TokenBody(data)
    except jwt.ExpiredSignatureError as e:
        print("expired")
        return "token expired"
    except Exception as e:
        return "token invalid"


def _resolve_request_body(request):
    return json.loads(request.body)


def _save_post(request_body: dict, token_body: TokenBody):
    # create db object
    new_post = Post()

    # find user
    user = find_user(token_body.email)

    if isinstance(user, User):
        new_post.author = user
        new_post.content = request_body['content']
        new_post.save()
        return True
    else:
        return False


def _get_all_posts():
    # all posts
    all_posts = Post.objects.all()

    posts = []

    # pack all posts into dict
    for _post in all_posts:
        _all_comments = _get_all_comments(_post)
        post_data = {
            'post_id': _post.id,
            'author': str(_post.author),
            'created': _format_time(_post.created),
            'last_updated': _format_time(_post.last_updated),
            'content': _post.content,
            'liked': _post.liked,
            'comments_count': len(_all_comments),
            'comments': _all_comments,
        }
        posts.append(post_data)

    return posts


def _get_all_comments(post: Post):
    _comments = []

    for comment in post.comment_set.all():
        _t2comments = _get_all_t2_comments(comment)
        comment_data = {
            'post_id': comment.post.id,
            'comment_id': comment.id,
            'author': str(comment.author),
            'created': _format_time(comment.created),
            'last_updated': _format_time(comment.last_updated),
            'content': comment.content,
            'liked': comment.liked,
            't2_comments_counts': len(_t2comments),
            't2_comments': _t2comments,
        }
        _comments.append(comment_data)

    return _comments


def _get_all_t2_comments(comment: Comment):
    _t2_comments = []

    for t2_comment in comment.t2comment_set.all():
        t2comment_data = {
            'comment_id': t2_comment.comment.id,
            't2_comment_id': t2_comment.id,
            'author': str(t2_comment.author),
            'created': _format_time(t2_comment.created),
            'last_updated': _format_time(t2_comment.last_updated),
            'content': t2_comment.content,
            'liked': t2_comment.liked,
        }
        _t2_comments.append(t2comment_data)

    return _t2_comments


def _format_time(time: datetime.datetime):
    return time.strftime('%Y-%m-%d %H:%M:%S')
