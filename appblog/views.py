from django.shortcuts import render, get_object_or_404, redirect

# ~/django/myProjects/blog1/appblog/forms.py
from .forms import PostForm, CommentForm

# from .models import Post, Comment
from .models import *

from django.contrib.auth.decorators import login_required
# from django.http import HttpResponse
# from django.template.loader import get_template
from django.utils import timezone

# from django.contrib.auth.models import User


# Create your views here.


# Listar post ordenado por fecha publicación
# def post_list(request):
#     posts = Post.objects.filter(
#         publish__lte=timezone.now()).order_by('publish')
#     return render(request, 'appblog/post_list.html', {'posts': posts})

# 👀 listar solo los que estan Published and are not Draft
# 💡 Utilizo el custom manager "published" que definí en "models.py"
def post_list(request):
    posts = Post.published.all()
    return render(request, 'appblog/post_list.html', {'posts': posts})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'appblog/post_detail.html', {'post': post})


@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.publish = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'appblog/post_edit.html', {'form': form})


@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.publis = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'appblog/post_edit.html', {'form': form})


@login_required
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')


# @permission_required
@login_required
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'appblog/add_comment_to_post.html', {'form': form})


@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)


@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('post_detail', pk=comment.post.pk)


# def login_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=None):
    """
    Decorator for views that checks that the user is logged in, redirecting
    to the log-in page if necessary.
    """

# def permission_required(perm, login_url=None, raise_exception=False):
    """
    Decorator for views that checks whether a user has a particular permission
    enabled, redirecting to the log-in page if necessary.
    If the raise_exception parameter is given the PermissionDenied exception
    is raised.
    """


def login(request):
    # 👇 esta vez le pasa a render solo un request y una url.
    return render(request, "registration/login.html")


def about_us(request):
    # 👇 esta vez le pasa a render solo un request y una url.
    return render(request, "appblog/about_us.html")


# --------------------
# categorías
#     Objetivos del Milenio
#     ONU
#     Organización internacional

# $ python manage.py shell
# >>> from appblog.models import Post

# --------------------
def filter_by_category_two(request):
    # posts = Post.objects.filter(category='onu')
    # posts = Post.objects.filter(category__startswith='onu')
    posts = Post.published.filter(category__startswith='objetivo')
    return render(request, 'appblog/post_list.html', {'posts': posts})


# --------------------
def filter_by_category(request):
    posts = Post.objects.all().order_by('category')
    return render(request, 'appblog/post_list.html', {'posts': posts})


def filter_by_category_reverse(request):
    posts = Post.objects.all().order_by('-category')
    return render(request, 'appblog/post_list.html', {'posts': posts})


# --------------------
def filter_by_title(request):
    posts = Post.objects.all().order_by('title')
    return render(request, 'appblog/post_list.html', {'posts': posts})


def filter_by_title_reverse(request):
    posts = Post.objects.all().order_by('-title')
    return render(request, 'appblog/post_list.html', {'posts': posts})


# --------------------
def filter_by_created(request):
    posts = Post.objects.all().order_by('created')
    return render(request, 'appblog/post_list.html', {'posts': posts})


def filter_by_created_reverse(request):
    posts = Post.objects.all().order_by('-created')
    return render(request, 'appblog/post_list.html', {'posts': posts})


# --------------------
def filter_by_publish(request):
    posts = Post.objects.all().order_by('publish')
    return render(request, 'appblog/post_list.html', {'posts': posts})


def filter_by_publish_reverse(request):
    posts = Post.objects.all().order_by('-publish')
    return render(request, 'appblog/post_list.html', {'posts': posts})


# --------------------
def filter_by_updated(request):
    posts = Post.objects.all().order_by('updated')
    return render(request, 'appblog/post_list.html', {'posts': posts})


def filter_by_updated_reverse(request):
    posts = Post.objects.all().order_by('-updated')
    return render(request, 'appblog/post_list.html', {'posts': posts})


# --------------------
# --------------------
# --------------------
# 💡💡💡 top 3 post by comments
# def GetTopPost(request):
def filter_by_number_of_comments(request):
    posts = Post.objects.raw(
        'SELECT appblog_post.*, (SELECT count(*) FROM appblog_comment WHERE appblog_comment.post_id = appblog_post.id) AS comentario FROM appblog_post ORDER BY comentario DESC LIMIT 3')
    return render(request, 'appblog/post_list.html', {'posts': posts})
