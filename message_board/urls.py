"""message_board URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from board.views import board_view, board_login_view, comment_view
from account.views import register_view, register_result_view, \
    login_view

urlpatterns = [
    path('admin/', admin.site.urls),

    path('board/', board_view),
    path('board/<str:name>/', board_login_view),
    path('board/<str:name>/comment/', comment_view),

    path('register/', register_view),
    path('register/result/', register_result_view),

    path('login/', login_view),
]
