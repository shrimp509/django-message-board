from django.shortcuts import render
from django.core.handlers.wsgi import WSGIRequest
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from .models import User
from .form_checker import check_register_data
import json


@csrf_exempt
def register_result_view(request: WSGIRequest):
    if request.method == "GET":
        return JsonResponse({"first": "string data", 10: "Hello"})
    elif request.method == "POST":
        decoded_body = json.loads(request.body)
        return JsonResponse({"get your post data": decoded_body})

    return JsonResponse({"status": "wrong"})


def login_view(request):
    return render(request, 'login.html', {})
