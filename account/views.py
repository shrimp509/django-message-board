from django.shortcuts import render, redirect
from django.core.handlers.wsgi import WSGIRequest
# from django.views.decorators.csrf import csrf_exempt

from .forms import UserForm


def register_view(request):
    return render(request, "register.html", {})


def register_send_view(request: WSGIRequest):
    user_form = UserForm(request.POST or None)
    if user_form.is_valid():
        check_register_data(user_form)
    else:
        print("errors: ", user_form.errors)
        print("error, get data: ", user_form.data)

    # return render(request, "register.html", {})
    return redirect("/register/")


def login_view(request):
    return render(request, 'login.html', {})


def check_register_data(form: UserForm):
    print("form valid, get data: ", form.data)

    # check account format
    account = form.data.get('account')
    if len(account) > 30:
        return False

    # check password format
    password = form.data.get('password')
    if len(password) > 30:
        return False

    # check birthday format
    form.data.get('birthday')

    # check phone format
    form.data.get('phone')

    # check email format
    form.data.get('email')

    # check first name format
    form.data.get('first_name')

    # check last name format
    form.data.get('last_name')

    return True