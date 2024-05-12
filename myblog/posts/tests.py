from django.test import TestCase, Client
from .models import Post, Follow
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.cache import cache
# Create your tests here.


class TestStringMethods(TestCase):
    def test_length(self):
        self.assertEqual(len('MyBlog'), 6)

    def test_show_msg(self):
        # действительно ли первый аргумент — True?
        self.assertTrue(False, msg="Важная проверка на истинность")

class ProfileTest(TestCase):
    
    def setUp(self):
        # 1-й пользователь
        # создание тестового клиента — подходящая задача для функции setUp()
        self.client = Client()
        # создаём пользователя
        self.user = User.objects.create_user(
            username="sarah", email="connor.s@skynet.com", password="KEKW_008"
        )
        # создаём пост от имени пользователя
        self.post = Post.objects.create(text="You're talking about things I haven't done yet in the past tense. It's driving me crazy!", author=self.user)

        # 2-й пользователь
        # создание тестового клиента — подходящая задача для функции setUp()
        self.client_2 = Client()
        # создаём пользователя
        self.user_2 = User.objects.create_user(
            username="max", email="notconnor.s@skynet.com", password="KEKW_009"
        )
        # создаём пост от имени пользователя
        self.post_2 = Post.objects.create(text="Second user", author=self.user_2)

    def test_profile(self):
        # формируем GET-запрос к странице сайта
        response = self.client.get("/sarah/")

        # проверяем что страница найдена
        self.assertEqual(response.status_code, 200)

        #print(response.context.keys())

        # проверяем, что при отрисовке страницы был получен список из 1 записи
        self.assertEqual(response.context["num_of_posts"], 1)

        # проверяем, что объект пользователя, переданный в шаблон, 
        # соответствует пользователю, которого мы создали
        self.assertIsInstance(response.context["user_profile"], User)
        self.assertEqual(response.context["user_profile"].username, self.user.username)

    def test_creating_post_when_authenticated(self):
        #----------- Начало: Вход в аккаунт--------------
        self.client.login(username='sarah', password='KEKW_008')
        response = self.client.get('')

        # Проверка, что зашёл нужный пользователь
        self.assertTrue('user' in response.context)
        self.assertEqual(response.context['user'].username, self.user.username)
        #----------- Конец: Вход в аккаунт--------------

        #----------- Начало: Создание поста--------------
        # Получаем URL страницы поста
        url = reverse('new_post')
        #print(url)

        # Отправляем GET-запрос на страницу изменения поста
        response = self.client.get(url)
        #print(response.context.keys())

        # проверяем, что страница найдена
        self.assertEqual(response.status_code, 200)

        # Текст нового поста
        new_text = "Created Post!"

        response = self.client.post(url, {'text': new_text})
        #print(response)
        #----------- Конец: Создание поста--------------

        #----------- Начало: Отображение поста--------------
        # формируем GET-запрос к странице сайта
        response = self.client.get("/sarah/")

        # проверяем что страница найдена
        self.assertEqual(response.status_code, 200)

        #print(response.context["page"][0].text)
        # проверяем, что при отрисовке страницы был получен список из 1 записи
        self.assertEqual(response.context["page"][0].text, new_text)
        #----------- Конец: Отображение в профиле--------------

    def test_creating_post(self):
        # Когда пост создан, он должен появиться на главной странице,
        # в профиле и в отдельном посте

        #----------- Начало: Отображение в профиле--------------
        # формируем GET-запрос к странице сайта
        response = self.client.get("/sarah/")

        # проверяем что страница найдена
        self.assertEqual(response.status_code, 200)

        # проверяем, что при отрисовке страницы был получен список из 1 записи
        self.assertEqual(response.context["num_of_posts"], 1)
        #----------- Конец: Отображение в профиле--------------

        #----------- Начало: Отображение на главной странице--------------
        # формируем GET-запрос к странице сайта
        response = self.client.get("")

        # проверяем что страница найдена
        self.assertEqual(response.status_code, 200)

        # print(response.context.keys())
        # print(response.context["page"][-1].author.username)
        # print(self.user.username)

        # проверяем, что последний пост принадлежит нашему пользователю
        self.assertEqual(response.context["page"][0].author.username, self.user.username)
        #----------- Конец: Отображение на главной странице--------------

        #----------- Начало: Отображение на отдельной странице поста--------------
        # Получаем URL страницы поста
        url = reverse('post', kwargs={'username': self.user.username, 'post_id': self.post.id})
        #print(url)

        # Отправляем GET-запрос на страницу поста
        response = self.client.get(url)
        #print(response.context.keys())

        # проверяем что страница найдена
        self.assertEqual(response.status_code, 200)

        # проверяем, что пост принадлежит нашему пользователю
        self.assertEqual(response.context["post"].author.username, self.user.username)

        #----------- Конец: Отображение на отдельной странице поста--------------

    def test_edit_post(self):
        # Проверка на возможно изменения поста зарегистрированному пользователю
        # Изменения отображаются на всех страницах
        
        #----------- Начало: Вход в аккаунт--------------
        self.client.login(username='sarah', password='KEKW_008')
        response = self.client.get('')

        self.assertTrue('user' in response.context)
        self.assertEqual(response.context['user'].username, self.user.username)
        #----------- Конец: Вход в аккаунт--------------


        #----------- Начало: Изменение поста--------------
        # Получаем URL страницы поста
        url = reverse('post_edit', kwargs={'username': self.user.username, 'post_id': self.post.pk})
        #print(url)

        # Отправляем GET-запрос на страницу изменения поста
        response = self.client.get(url)
        #print(response.context.keys())

        # проверяем, что страница найдена
        self.assertEqual(response.status_code, 200)

        # Текст нового поста
        new_text = "New Post!"

        response = self.client.post(url, {'text': new_text})
        #print(response)
        #----------- Конец: Изменение поста--------------

        #----------- Начало: Отображение в профиле--------------
        # формируем GET-запрос к странице сайта
        response = self.client.get("/sarah/")

        # проверяем что страница найдена
        self.assertEqual(response.status_code, 200)

        # проверяем, что теперь здесь новая запись
        self.assertEqual(response.context["page"][0].text, new_text)
        #----------- Конец: Отображение в профиле--------------

        #----------- Начало: Отображение на главной странице--------------
        # формируем GET-запрос к странице сайта
        response = self.client.get("")

        # проверяем что страница найдена
        self.assertEqual(response.status_code, 200)

        # проверяем, что последний пост принадлежит нашему пользователю
        self.assertEqual(response.context["page"][0].text, new_text)
        #----------- Конец: Отображение на главной странице--------------

        #----------- Начало: Отображение на отдельной странице поста--------------
        # Получаем URL страницы поста
        url = reverse('post', kwargs={'username': self.user.username, 'post_id': self.post.id})

        # Отправляем GET-запрос на страницу поста
        response = self.client.get(url)
        #print(response.context.keys())

        # проверяем что страница найдена
        self.assertEqual(response.status_code, 200)

        # проверяем, что пост принадлежит нашему пользователю
        self.assertEqual(response.context["post"].text, new_text)
        #----------- Конец: Отображение на отдельной странице поста--------------

    def test_creating_post_when_not_authenticated(self):
        # Сайт должен не позволить создать пост и перенаправить
        # на страницу входа в аккаунт

        # Получаем URL для создания поста
        url = reverse('new_post')
        #print(url)

        # Отправляем POST-запрос на URL создания поста
        response = self.client.post(url, {'text': 'Test post content'}) 
        #print(response)

        # Проверяем, что произошел редирект
        self.assertEqual(response.status_code, 302)

        # Проверяем, что редирект ведет на страницу входа
        # После входа в аккаунт, редиректит обратно к созданию поста
        self.assertRedirects(response, f"{reverse('login')}?next={url}")

    def test_error_404(self):
        # формируем GET-запрос к странице сайта
        response = self.client.get("/LOL/CHTO")
        #print(response)

        # Проверяем, что произошла ошибка 404
        self.assertEqual(response.status_code, 404)

    def test_follow_unfollow(self):
        #----------- Начало: Вход в аккаунт--------------
        self.client.login(username='sarah', password='KEKW_008')
        response = self.client.get('')

        self.assertTrue('user' in response.context)
        self.assertEqual(response.context['user'].username, self.user.username)
        #----------- Конец: Вход в аккаунт--------------

        #Проверка на подписку
        before = Follow.objects.all().count()
        url = reverse('profile_follow', kwargs={'username': self.user_2.username})
        self.client.get(url)
        after = Follow.objects.all().count()
        self.assertEqual(before + 1, after)

        #Проверка на отписку
        url = reverse('profile_unfollow', kwargs={'username': self.user_2.username})
        self.client.get(url)
        after = Follow.objects.all().count()
        self.assertEqual(before, after)




    # def test_index_page_cache(self):
    #     # Очистим кэш перед тестом
    #     cache.clear()

    #     # Первый запрос - страница должна быть сгенерирована
    #     response = self.client.get('/')
    #     self.assertContains(response, "Последние обновления на сайте")
    #     self.assertEqual(response.status_code, 200)

    #     # Второй запрос - страница должна быть взята из кэша
    #     response = self.client.get('/')
    #     self.assertContains(response, "Последние обновления на сайте")
    #     self.assertEqual(response.status_code, 200)

    #     # Удалим запись из кэша
    #     cache.delete('index_page')

    #     # Третий запрос - страница снова должна быть сгенерирована
    #     response = self.client.get('/')
    #     self.assertContains(response, "Последние обновления на сайте")
    #     self.assertEqual(response.status_code, 200)


    # def test_image_display_everywhere(self):
        
    #     #----------- Начало: Вход в аккаунт--------------
    #     self.client.login(username='sarah', password='KEKW_008')
    #     response = self.client.get('')

    #     self.assertTrue('user' in response.context)
    #     self.assertEqual(response.context['user'].username, self.user.username)
    #     #----------- Конец: Вход в аккаунт--------------
       
    #     #----------- Начало: Изменение поста--------------
    #     # Получаем URL страницы поста
    #     url = reverse('post_edit', kwargs={'username': self.user.username, 'post_id': self.post.pk})
    #     #print(url)

    #     # Отправляем GET-запрос на страницу изменения поста
    #     response = self.client.get(url)
    #     #print(response.context.keys())

    #     # проверяем, что страница найдена
    #     self.assertEqual(response.status_code, 200)

    #     with open('posts/media/file.jpg','rb') as img:
    #         response = self.client.post(url, {'text': 'post with image', 'image': img})

    #     #print(response)
    #     #----------- Конец: Изменение поста--------------


    #     #----------- Начало: Отображение в профиле--------------
    #     # формируем GET-запрос к странице сайта
    #     response = self.client.get("")

    #     # проверяем что страница найдена
    #     self.assertEqual(response.status_code, 200)

    #     print(response.content)

    #     #print(response.context["page"][0].image)
    #     self.assertContains(response.content, '<img>')

    #     #----------- Конец: Отображение в профиле--------------

    #     #----------- Начало: Отображение на главной странице--------------
    #     # формируем GET-запрос к странице сайта
    #     response = self.client.get("")

    #     # проверяем что страница найдена
    #     self.assertEqual(response.status_code, 200)

    #     # print(response.context.keys())
    #     # print(response.context["page"][-1].author.username)
    #     # print(self.user.username)

    #     # проверяем, что последний пост принадлежит нашему пользователю
    #     self.assertEqual(response.context["page"][0].author.username, self.user.username)
    #     #----------- Конец: Отображение на главной странице--------------

    #     #----------- Начало: Отображение на отдельной странице поста--------------
    #     # Получаем URL страницы поста
    #     url = reverse('post', kwargs={'username': self.user.username, 'post_id': self.post.id})
    #     #print(url)

    #     # Отправляем GET-запрос на страницу поста
    #     response = self.client.get(url)
    #     #print(response.context.keys())

    #     # проверяем что страница найдена
    #     self.assertEqual(response.status_code, 200)

    #     # проверяем, что пост принадлежит нашему пользователю
    #     self.assertEqual(response.context["post"].author.username, self.user.username)

    #     #----------- Конец: Отображение на отдельной странице поста--------------