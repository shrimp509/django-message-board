from .models import Post, Comment, T2Comment
from django.db.models import Model


def find_post(id: int):
    return _find_resources(Post, id)


def find_comment(id: int):
    return _find_resources(Comment, id)


def find_t2_comment(id: int):
    return _find_resources(T2Comment, id)


def _find_resources(res: Model, id: int):
    exist = res.objects.filter(id=id)

    err_msg = None

    if len(exist) == 0:
        err_msg = "{} not found".format(type(res).__name__)

    for res in exist:
        return res

    return err_msg