from django.core.handlers.wsgi import WSGIRequest
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from .models import User
from .form_checker import check_register_data
import json


@csrf_exempt
def register(request: WSGIRequest):
    return ""


