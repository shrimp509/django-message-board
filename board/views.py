from django.shortcuts import render
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponseRedirect

from .models import Post, Comment
from .forms import PostForm, CommentForm


def board_view(request: WSGIRequest):
    # post form
    post_form = PostForm(request.POST or None)
    if post_form.is_valid():
        post_form.save()

    posts = get_posts()

    return render(request, 'board.html', context={"name": None, 'post_form': post_form, 'posts': posts})


def board_login_view(request: WSGIRequest, name):
    # post form
    post_form = PostForm(request.POST or None)
    if post_form.is_valid():
        post = Post()
        post.content = post_form.data.get('content')
        post.publisher = name
        post.save()
    else:
        print("post form is not valid")

    # get all post and comments
    posts = get_posts()
    comments = get_comments()

    print("posts: ", posts[0].id)
    print("comments: ", comments)

    # render page
    return render(request, 'board.html',
                  context={"name": name, 'post_form': post_form,
                           'posts': posts, 'comments': comments})


def get_posts():
    return Post.objects.all()


def get_comments():
    return Comment.objects.all()


def comment_view(request: WSGIRequest, name):
    comment_form = CommentForm(request.POST or None)
    if comment_form.is_valid():
        create_comment(name, comment_form.data.get('content'), comment_form.data.get("post_id"))
    else:
        print("comment form is not valid")

    return HttpResponseRedirect("/board/" + name)


def create_comment(name, comment, post_id):
    new_comment = Comment()
    new_comment.content = comment
    new_comment.publisher = name
    new_comment.post_id = post_id
    new_comment.save()


