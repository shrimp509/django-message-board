from django.shortcuts import render, redirect
from django.core.handlers.wsgi import WSGIRequest
# from django.views.decorators.csrf import csrf_exempt
from .form_checker import check_register_data

from .forms import UserForm


def register_view(request):
    return render(request, "register.html", {})


def register_send_view(request: WSGIRequest):
    user_form = UserForm(request.POST or None)
    if user_form.is_valid():
        if check_register_data(user_form):
            print("data checked, save to model")
            user_form.save()
        else:
            print("data checkd error")
    else:
        print("errors: ", user_form.errors)
        print("error, get data: ", user_form.data)

    return redirect("/register/")


def login_view(request):
    return render(request, 'login.html', {})

