import json
import jwt
import time

from django.core.handlers.wsgi import WSGIRequest
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from message_board import settings
from .data_checker import check_register_data, check_login_data, find_user
from .models import User

'''
Get `Email` and `Password` from request body
then, return a JWT token
'''
@csrf_exempt
def login(request: WSGIRequest):
    if request.method == "POST":
        account = json.loads(request.body)
        err_msg = check_login_data(account)

        if err_msg is None:

            user = find_user(account['email'])

            if isinstance(user, User):
                return _return_status("Login succeed",
                                      name=find_user(account['email']).name,
                                      token=_get_token(
                                          account['email'],
                                          account['password']
                                      ))
            else:
                return _return_status("Login failed", err_msg=user)
        else:
            return _return_status("Login failed", err_msg)

'''
Get 'Email', 'Password' and 'Name' from request body
then, return a status
'''
@csrf_exempt
def register(request: WSGIRequest):
    if request.method == "POST":
        user = json.loads(request.body)

        # analyze data format
        try:
            err_msg = check_register_data(user)
        except Exception as e:
            return _return_status("Please contact backend developer, Wrong field format, raw error: {}".format(e))

        # save to db if valid
        if err_msg is None:
            _dict2object_user(user).save()
            return _return_status("User created")
        else:
            return _return_status("Wrong field", err_msg)

    return _return_status("Wrong method", err_msg="no GET method in register")


# #############################
# Private methods
# #############################

def _return_status(message: str, err_msg=None, **kwargs):
    if err_msg is None and kwargs is None:
        return JsonResponse({"status": message})
    elif err_msg is not None and kwargs is None:
        return JsonResponse({"status": message, "err_msg": err_msg})
    elif err_msg is None and kwargs is not None:
        msg = {"stauts": message}
        for key, value in kwargs.items():
            msg[key] = value
        return JsonResponse(msg)
    else:
        msg = {"status": message, "err_msg": err_msg}
        for key, value in kwargs.items():
            msg[key] = value
        return JsonResponse(msg)


def _dict2object_user(user_dict):
    user = User()
    user.name = user_dict['name']
    user.password = user_dict['password']
    user.email = user_dict['email']
    return user


def _get_token(email: str, password: str):
    return jwt.encode({'email': email, 'password': password, 'exp': int(time.time()) + 86400 * 7}, settings.SECRET_KEY, 'HS256').decode('UTF-8')
