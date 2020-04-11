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

from account.apis import register, login, logout
from board.apis import post, comment, t2_comment, like, edit, delete

api_path = 'api/v1/'

urlpatterns = [
    path('admin/', admin.site.urls),

    path(api_path + 'register/', register),
    path(api_path + 'register', register),

    path(api_path + 'login/', login),
    path(api_path + 'login', login),

    path(api_path + 'logout/', logout),
    path(api_path + 'logout', logout),

    path(api_path + 'board/post/', post),
    path(api_path + 'board/post', post),

    path(api_path + 'board/post/<int:post_id>/comment/', comment),
    path(api_path + 'board/post/<int:post_id>/comment', comment),

    path(api_path + 'board/comment/<int:comment_id>/t2_comment/', t2_comment),
    path(api_path + 'board/comment/<int:comment_id>/t2_comment', t2_comment),

    path(api_path + 'board/like/<str:resource>/<int:id>', like),
    path(api_path + 'board/like/<str:resource>/<int:id>/', like),

    path(api_path + 'board/edit/<str:resource>/<int:id>', edit),
    path(api_path + 'board/edit/<str:resource>/<int:id>/', edit),

    path(api_path + 'board/delete/<str:resource>/<int:id>', delete),
    path(api_path + 'board/delete/<str:resource>/<int:id>/', delete),
]
