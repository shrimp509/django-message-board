import jwt
import json

from django.core.handlers.wsgi import WSGIRequest
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from message_board.settings import SECRET_KEY

from .models import Post
from account.data_checker import find_user
from account.models import User


# #####################
#   APIs
# #####################
@csrf_exempt
def post(request: WSGIRequest):
    if request.method == 'GET':
        return _return_status('this is GET method of post, not yet implemented')
    elif request.method == 'POST':

        token_body = _resolve_jwt(request.headers.get('token'))

        if type(token_body) is TokenBody:
            # valid token
            request_body = _resolve_request_body(request)
            try:
                if save_post(request_body, token_body):
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


def _resolve_request_body(request):
    return json.loads(request.body)


def save_post(request_body: dict, token_body: TokenBody):
    # create db object
    new_post = Post()

    # find user
    user = find_user(token_body.email)

    if user is User:
        new_post.author = user
        new_post.content = request_body['content']
        new_post.save()
        return True
    else:
        return False
