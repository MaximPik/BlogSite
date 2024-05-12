from django.contrib import admin
# из файла models импортируем модель Post
from .models import Post, Group

class PostAdmin(admin.ModelAdmin):
    # перечисляем поля, которые должны отображаться в админке
    list_display = ("pk","text", "pub_date", "author", "group")
    # добавляем интерфейс для поиска по тексту постов
    search_fields = ("text",)
    # добавляем возможность фильтрации по дате
    list_filter = ("pub_date",)
    empty_value_display = "-пусто-" # это свойство сработает для всех колонок: где пусто - там будет эта строка

admin.site.register(Post, PostAdmin)

class GroupAdmin(admin.ModelAdmin):
    list_display = ("title", "description", "slug")

    search_fields = ("title", "description",)

    list_filter = ("title",)

    empty_value_display = "-пусто-" # это свойство сработает для всех колонок: где пусто - там будет эта строка

    prepopulated_fields = {'slug': ('title',)}  # Автоматическое заполнение slug на основе title
    
admin.site.register(Group, GroupAdmin)

