from django.core.handlers.wsgi import WSGIRequest
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from .models import User
from .data_checker import check_register_data
import json


@csrf_exempt
def register(request: WSGIRequest):
    if request.method == "POST":
        user = json.loads(request.body)
        print("user type: ", type(user))

        # analyze data format
        try:
            err_msg = check_register_data(user)
        except Exception as e:
            return return_status("Please contact backend developer, Wrong field format, raw error: {}".format(e))

        # save to db if valid
        if err_msg is None:
            dict2object_user(user).save()
            return return_status("User created")
        else:
            return return_status("Wrong field", err_msg)

    return return_status("Wrong method", err_msg="no GET method in register")


def return_status(message: str, err_msg=None):
    if err_msg is None:
        return JsonResponse({"status": message})
    else:
        return JsonResponse({"status": message, "err_msg": err_msg})


def dict2object_user(user_dict):
    user = User()
    user.name = user_dict['name']
    user.password = user_dict['password']
    user.email = user_dict['email']
    return user
