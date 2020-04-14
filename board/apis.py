import jwt
import json
import datetime

from django.core.handlers.wsgi import WSGIRequest
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import models

from message_board.settings import SECRET_KEY
from .models import Post, Comment, T2Comment
from account.data_checker import find_user
from account.models import User, BlackList

# #####################
#   Global Variables
# #####################
resources = ["post", "comment", "t2_comment"]

# #####################
#   APIs
# #####################
@csrf_exempt
def post(request: WSGIRequest):
    if request.method == 'GET':
        all_posts = _get_all_posts()
        return _return_status('Get posts succeed', posts=all_posts)
    elif request.method == 'POST':

        token_body = _resolve_jwt(request.headers.get('Authorization'))

        if type(token_body) is TokenBody:
            # valid token
            request_body = _resolve_request_body(request)
            try:
                if _save_post(request_body, token_body):
                    return _return_status('Post created')
                else:
                    return _return_status('Failed to create Post',
                                          err_msg='unexpected error, please contact backend developer')
            except KeyError as e:
                return _return_status('Wrong request body format', err_msg='body should be `content`')
        else:
            # invalid token
            return _return_status('Invalid token', err_msg='token invalid or expired: {}'.format(token_body))
    else:
        return _return_status('No such method')


@csrf_exempt
def comment(request: WSGIRequest, post_id: int):
    if request.method == 'POST':
        # check token
        token_body = _resolve_jwt(request.headers.get('Authorization'))

        if type(token_body) is TokenBody:
            # check post_id exist
            post_exist = _find_model_exist(Post, id=post_id)
            if post_exist is None:
                return _return_status('No such post_id: {}'.format(post_id))
            else:
                # check user exist
                user_exist = _find_model_exist(User, email=token_body.email)
                if user_exist is None:
                    return _return_status("No such email: {}".format(token_body.email))
                else:
                    try:
                        # save comment and related to that post_id, if post_id exist
                        result = _save_comment(post_exist, user_exist, json.loads(request.body)['content'])
                        if result:
                            return _return_status("Comment created")
                        else:
                            return _return_status("Failed to create comment",
                                                  err_msg='unexpected error, please contact backend developer')
                    except KeyError as e:
                        return _return_status("Wrong request body format", err_msg='body should be `content`')
        else:
            return _return_status("Invalid token", err_msg='token invalid or expired: {}'.format(token_body))
    else:
        return _return_status("No such method")


@csrf_exempt
def t2_comment(request: WSGIRequest, comment_id: int):
    if request.method == "POST":
        # check token
        token_body = _resolve_jwt(request.headers.get('Authorization'))

        if type(token_body) is TokenBody:
            # check comment_id exist
            comment_exist = _find_model_exist(Comment, id=comment_id)
            if comment_exist is None:
                return _return_status("No such comment_id: {}".format(comment_id))
            else:
                # check user exist
                user_exist = _find_model_exist(User, email=token_body.email)
                if user_exist is None:
                    return _return_status("No such email: {}".format(token_body.email))
                else:
                    try:
                        # save t2 comment and related to that comment_id, if comment_id exist
                        result = _save_t2comment(comment_exist, user_exist, json.loads(request.body)['content'])
                        if result:
                            return _return_status("T2Comment created")
                        else:
                            return _return_status("Failed to create t2 comment",
                                                  err_msg='unexpected error, please contact backend developer')
                    except KeyError as e:
                        return _return_status("Wrong request body format", err_msg='body should be `content`')
        else:
            return _return_status("Invalid token", err_msg='token invalid or expired: {}'.format(token_body))
    else:
        return _return_status("No such method")


@csrf_exempt
def like(request: WSGIRequest, resource: str, id: int):
    result, added_likes = _check_request_format(request, "PATCH", resource, id, 'add', int)
    if type(result) is JsonResponse:
        return result
    else:
        res = result

        # update likes into db
        res.liked = int(res.liked) + added_likes
        res.save()
        return _return_status("like updated")


@csrf_exempt
def edit(request: WSGIRequest, resource: str, id: int):
    result, content = _check_request_format(request, "PATCH", resource, id, 'content', str)
    if type(result) is JsonResponse:
        return result
    else:
        res = result

        # update content into db
        res.content = content
        res.save()
        return _return_status("Content updated")


@csrf_exempt
def delete(request: WSGIRequest, resource: str, id: int):
    result, _ = _check_request_format(request, "DELETE", resource, id, None, None)
    if type(result) is JsonResponse:
        return result
    else:
        res = result

        # delete obj in db
        res.delete()
        return _return_status("{} id={} deleted".format(resource, id))


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

        if BlackList.objects.filter(token=token).exists():
            return "token expired"

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


def _find_model_exist(model: models.Model, **conditions):
    if len(conditions) == 1:
        for key, value in conditions.items():
            exist = model.objects.filter(**{key: value})
            for obj in exist:
                return obj
        return None
    else:
        raise AttributeError("Only can throw one conditions")


def _save_comment(belonged_post: Post, user: User, content: str):
    try:
        # create db object
        new_comment = Comment()
        new_comment.post = belonged_post
        new_comment.author = user
        new_comment.content = content
        new_comment.save()
        return True
    except Exception as e:
        return False


def _save_t2comment(belonged_comment: Comment, user: User, content: str):
    try:
        # create db object
        new_comment = T2Comment()
        new_comment.comment = belonged_comment
        new_comment.author = user
        new_comment.content = content
        new_comment.save()
        return True
    except Exception as e:
        return False


def _check_request_format(request: WSGIRequest, method: str, resource: str, id: int, field: str, field_type: object):
    # check token
    token = request.headers.get('Authorization')
    if token is None:
        return _return_status("Wrong header format", err_msg="headers should contain `Authorization` field"), None
    else:
        result = _resolve_jwt(token)
        if type(result) is not TokenBody:
            return _return_status("Token invalid or expired: {}".format(result)), None

    # check all
    if request.method == method:
        if resource in resources:
            # check id exist
            from .data_checker import find_post, find_comment, find_t2_comment
            if resource == resources[0]:
                msg = find_post(id)
            elif resource == resources[1]:
                msg = find_comment(id)
            elif resource == resources[2]:
                msg = find_t2_comment(id)
            else:
                msg = "No this resource"

            if type(msg) == Post or type(msg) == Comment or type(msg) == T2Comment:
                res = msg
                try:
                    body_field = json.loads(request.body)[field]
                    if type(body_field) is not field_type:
                        return _return_status("Wrong body format", err_msg="`{}` field should be `{}`".format(field, field_type)), None
                    else:
                        return res, body_field
                except KeyError as e:
                    if field is None and field_type is None:
                        return res, None
                    return _return_status("Wrong body format", err_msg="should contains `{}` field".format(field)), None
                except Exception as e:
                    if field is None and field_type is None:
                        return res, None
                    return _return_status("Unexpected error, please contact backend developer"), None
            else:
                return _return_status("Wrong id", err_msg="{} id={} not found".format(resource, id)), None
        else:
            return _return_status("Wrong resources", err_msg="resources should be `post` or `comment` or `t2_comment`"), None
    else:
        return _return_status("No such method"), None
