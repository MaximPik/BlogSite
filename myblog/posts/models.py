from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Group(models.Model):
    # Дабавление заголовка с обязательным заполнением
    title = models.TextField(blank=False, null=False)
    # Описание группы
    description = models.TextField()
    # Свойство уникального URL адреса. group/
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.title

# Create your models here.
class Post(models.Model):
    # свойство text типа TextField
    text = models.TextField()
    # Свойство group. Ссылаемся на Group
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, blank=True, null=True)
    # свойство pub_date типа DateTimeField, текст "date published" это заголовок
    # поля в интерфейсе администратора. auto_now_add говорит, что при создании
    # новой записи автоматически будет подставлено текущее время и дата
    pub_date = models.DateTimeField("date published", auto_now_add = True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    image = models.ImageField(upload_to='posts/media/', blank=True, null=True)
    
class Comment(models.Model):
    # Ссылка на пост
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    # Ссылка на автора комментария
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    # Текст комментария
    text = models.TextField()
    # Дата и время
    created = models.DateTimeField(auto_now_add = True)

class Follow(models.Model):
    # ссылка на объект пользователя, который подписывается.
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="follower")
    # ссылка на объект пользователя, на которого подписываются
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")

