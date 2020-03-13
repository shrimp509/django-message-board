from django.shortcuts import render

from board.views import board_view, board_login_view
from django.http import HttpResponseRedirect

from login.forms import UserForm


def login_view(request):
    # user form
    form = UserForm(request.POST or None)
    if form.is_valid():
        return HttpResponseRedirect("/board/" + form.data.get('username'))

    return render(request, 'login.html', context={'form': form})

