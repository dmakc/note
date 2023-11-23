from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from notes.models import Note

User = get_user_model()


class TestRoutes(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Автор')
        cls.reader = User.objects.create(username='Юзер')
        cls.note = Note.objects.create(
            title='Заголовок',
            text='Текст заметки',
            slug='note-slug',
            author=cls.author,
        )
        cls.args_slug = cls.note.slug,

    def test_availability_for_comment_edit_and_delete(self):
        users_statuses = (
            (self.author, HTTPStatus.OK),
            (self.reader, HTTPStatus.NOT_FOUND),
        )
        for user, status in users_statuses:
            self.client.force_login(user)
            for name in ('notes:edit', 'notes:delete'):
                with self.subTest(user=user, name=name):
                    url = reverse(name, args=(self.note.id,))
                    response = self.client.get(url)
                    self.assertEqual(response.status_code, status)

    def test_redirect_for_anonymous_client(self):
        login_url = reverse('users:login')
        for name in (
            'notes:edit',
            'notes:delete',
            # 'notes:list',
            'notes:detail',
            # 'notes:success',
            # 'notes:add',
        ):
            with self.subTest(name=name):
                url = reverse(name, args=(self.note.id,))
                redirect_url = f'{login_url}?next={url}'
                response = self.client.get(url)
                self.assertRedirects(response, redirect_url)

    def test_pages_availability(self):
        urls = (
            ('notes:home', None),
            ('notes:detail', (self.note.id,)),
            ('users:login', None),
            ('users:logout', None),
            ('users:signup', None),
        )
        for name, args in urls:
            with self.subTest(name=name):
                url = reverse(name, args=args)
                response = self.client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)




# class TestRoutes(TestCase):

#     @classmethod
#     def setUpTestData(cls):
#         cls.author = User.objects.create(username='Автор')
#         cls.author_client = Client()
#         # cls.author_client.force_login(cls.author)
#         cls.user = User.objects.create(username='Читатель')
#         cls.auth_client = Client()
#         # cls.auth_client.force_login(cls.user)
#         cls.note = Note.objects.create(
#             title='Заголовок',
#             text='Текст заметки',
#             slug='note-slug',
#             author=cls.author,
#         )
#         cls.args_slug = cls.note.slug,

#     def test_pages_availability(self):
#         urls = (
#             ('notes:home', None),
#             ('notes:detail', (self.note.id,)),
#             ('users:login', None),
#             ('users:logout', None),
#             ('users:signup', None),
#         )
#         for name, args in urls:
#             with self.subTest(name=name):
#                 url = reverse(name, args=args)
#                 response = self.client.get(url)
#                 self.assertEqual(response.status_code, HTTPStatus.OK)

#     def test_availability_for_note_list_edit_and_delete(self):
#         users_statuses = (
#             (self.author, HTTPStatus.OK),
#             (self.user, HTTPStatus.NOT_FOUND),
#         )
#         for user, status in users_statuses:
#             # Логиним пользователя в клиенте:
#             self.client.force_login(user)
#             # Для каждой пары "пользователь - ожидаемый ответ"
#             # перебираем имена тестируемых страниц:
#             for name in ('notes:detail', 'notes:edit', 'notes:delete'):
#                 with self.subTest(user=user, name=name):
#                     url = reverse(name, args=(self.note.id,))
#                     response = self.client.get(url)
#                     self.assertEqual(response.status_code, status)

#     """Главная страница доступна анонимному пользователю."""
#     def test_home_page(self):
#         url = reverse('notes:home')
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, HTTPStatus.OK)
