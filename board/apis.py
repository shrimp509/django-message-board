import jwt

from django.core.handlers.wsgi import WSGIRequest
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from message_board.settings import SECRET_KEY


@csrf_exempt
def post(request: WSGIRequest):
    if request.method == 'GET':
        return _return_status('this is GET method of post')
    elif request.method == 'POST':

        try:
            data = jwt.decode(
                request.headers.get('token'),
                SECRET_KEY
            )
            print("data in token: ", data)
        except jwt.ExpiredSignatureError as e:
            print("expired")

        return _return_status('this is POST method of post')
    else:
        return _return_status('no such method')


# #####################
#   Private methods
# #####################
def _return_status(status: str, **kwargs):
    msg = {'status': status}
    for key, value in kwargs.items():
        msg[key] = value
    return JsonResponse(msg)
