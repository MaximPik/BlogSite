from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Post, Group, Comment, Follow
from .forms import PostForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib.auth import get_user_model
import datetime as dt
from django.contrib.auth.models import User
from django.views.decorators.cache import cache_page


User = get_user_model()

def index(request):
    post_list = Post.objects.order_by('-pub_date').all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, "index.html", {"page": page, "paginator": paginator})

def group_posts(request, slug):
    # # функция get_object_or_404 получает по заданным критериям объект из базы данных 
    # # или возвращает сообщение об ошибке, если объект не найден
    # group = get_object_or_404(Group, slug=slug)

    # # Метод .filter позволяет ограничить поиск по критериям. Это аналог добавления
    # # условия WHERE group_id = {group_id}
    # posts = Post.objects.filter(group=group).order_by("-pub_date")[:12]
    # return render(request, "group.html", {"group": group, "posts": posts})
    group = get_object_or_404(Group, slug=slug)
    post_list_group = Post.objects.filter(group=group).order_by('-pub_date').all()
    paginator = Paginator(post_list_group, 5)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(request, "group.html", {"page": page, "paginator": paginator, "group": group})


@login_required
def new_post(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect("index")
    else:
        form = PostForm()
    return render(request, "new_post.html", {"form": form})


@login_required
def post_edit(request, username, post_id):
    # #post = Post.objects.filter(pk=post_id)[0]
    # post = get_object_or_404(Post, pk=post_id)
    # if request.method == 'POST':
    #     form = PostForm(request.POST, instance=post)
    #     if form.is_valid():
    #         post = form.save(commit=False)
    #         post.author = request.user
    #         post.pub_date = dt.datetime.now()
    #         post.save()
    #         return redirect(f'/{username}/{post_id}')
    # else:
    #     form = PostForm(instance=post)

    # context = {
    #     "form": form,
    #     "post": post,
    # }
    profile = get_object_or_404(User, username=username)
    post = get_object_or_404(Post, pk=post_id, author=profile)
    if request.user != profile:
        return redirect('post', username=username, post_id=post_id)
    # добавим в form свойство files
    form = PostForm(request.POST or None, files=request.FILES or None, instance=post)
    
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect("post", username=request.user.username, post_id=post_id)
    
    context = {
        "form": form,
        "post": post,
    }    
    
    return render(request, "new_post.html", context)
    


def profile(request, username):
    user_profile = get_object_or_404(User, username=username)
    # Получаем список постов пользователя
    post_list = Post.objects.filter(author=user_profile).order_by('-pub_date').all()

    # Пагинация
    paginator = Paginator(post_list, 5)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    # Количество постов
    num_of_posts = post_list.count()

    # Определяем, может ли текущий пользователь редактировать профиль
    edit = request.user.is_authenticated and request.user == user_profile

    #Проверяем, есть ли у пользователя в подписках
    authors = Follow.objects.filter(user=request.user).values_list('author', flat=True)
    if user_profile.id in authors:
        following = True
    else:
        following = False
    
    authors = Follow.objects.filter(user=user_profile).values_list('author', flat=True)
    num_of_authors = authors.count()

    subs = Follow.objects.filter(author=user_profile).values_list('user', flat=True)
    num_of_subs = subs.count()

    context = {
        "page": page,
        "paginator": paginator,
        "num_of_posts": num_of_posts,
        "edit": edit,
        "user_profile": user_profile,  # Переименовал переменную для ясности
        "following": following,
        "num_of_subs": num_of_subs,
        "num_of_authors": num_of_authors,
    }

    return render(request, 'profile.html', context)
 
 
def post_view(request, username, post_id):
    user_profile = get_object_or_404(User, username=username)
    #Выбранный пост автора
    post = Post.objects.filter(pk=post_id)[0]
    #Список постов одного автора
    post_list = Post.objects.filter(author__username=username).order_by('-pub_date').all()
    #Количество постов
    num_of_posts = post_list.count()
    # Определяем, может ли текущий пользователь редактировать профиль
    edit = request.user.is_authenticated and request.user == user_profile
    # Комментарии к посту
    comments = post.comments.all().order_by('-created')
    form = CommentForm()

    context = {
        "post": post,
        "num_of_posts": num_of_posts,
        "user_profile": user_profile,  # Переименовал переменную для ясности
        "edit": edit,
        "comments": comments,
        "form": form,
    }

    return render(request, 'post.html', context)

def page_not_found(request, exception):
    # Переменная exception содержит отладочную информацию, 
    # выводить её в шаблон пользователской страницы 404 мы не станем
    return render(
        request, 
        "misc/404.html", 
        {"path": request.path}, 
        status=404
    )

def server_error(request):
    return render(request, "misc/500.html", status=500)

def add_comment(request, username, post_id):
    post = get_object_or_404(Post, pk=post_id, author__username=username)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post', username=username, post_id=post_id)
        
@login_required
def follow_index(request):
    #Вывод постов, на которые подписан пользователь
    # Получаем авторов, на которые подписан пользователь
    # authors = Follow.objects.filter(user=request.user).values_list('author', flat=True)
    authors = Follow.objects.filter(user=request.user)
    # Получаем посты этих авторов
    post_list_group = Post.objects.filter(author__following__in=authors).order_by('-pub_date').all()
    paginator = Paginator(post_list_group, 5)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    context = {
        "page": page,
        "paginator": paginator,
    }
    return render(request, "follow.html", context)

@login_required
def profile_follow(request, username):
    user_profile = get_object_or_404(User, username=username)
    # Проверяем, не пытается ли пользователь подписаться сам на себя
    if user_profile != request.user:
        # Используем get_or_create, чтобы не создавать дубликаты подписок
        Follow.objects.get_or_create(user=request.user, author=user_profile)
    return redirect('profile', username=username)


@login_required
def profile_unfollow(request, username):
    user_profile = get_object_or_404(User, username=username)
    # Удаляем подписку, если она существует
    Follow.objects.filter(user=request.user, author=user_profile).delete()
    return redirect('profile', username=username)