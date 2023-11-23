from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from notes.models import Note

User = get_user_model()


class TestRoutes(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.note = Note.objects.create(title='Заголовок', text='Текст')
        cls.author = User.objects.create(username='Лев Толстой')
        cls.reader = User.objects.create(username='Читатель простой')

    """Главная страница доступна анонимному пользователю."""
    def test_home_page(self):
        url = reverse('notes:home')
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
    
    def test_home_page(self):
        url = reverse('notes:list')
        response = self.reader.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
    
    def test_home_page(self):
        url = reverse('notes:success')
        response = self.reader.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
    
    def test_home_page(self):
        url = reverse('notes:add')
        response = self.reader.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    # """Страница отдельной заметки, удаления, редактирования доступна автору."""
    # def test_detail_page(self):
    #     url = reverse('notes:detail', args=(self.note.id,))
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, HTTPStatus.OK)

    # def test_availability_for_comment_edit_and_delete(self):
    #     users_statuses = (
    #         (self.author, HTTPStatus.OK),
    #         (self.reader, HTTPStatus.NOT_FOUND),
    #     )
    #     for user, status in users_statuses:
    #         # Логиним пользователя в клиенте:
    #         self.client.force_login(user)
    #         # Для каждой пары "пользователь - ожидаемый ответ"
    #         # перебираем имена тестируемых страниц:
    #         for name in ('notes:edit', 'notes:delete'):
    #             with self.subTest(user=user, name=name):
    #                 url = reverse(name, args=(self.note.id,))
    #                 response = self.client.get(url)
    #                 self.assertEqual(response.status_code, status)

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Автор')
        cls.author_client = Client()
        cls.author_client.force_login(cls.author)
        cls.user = User.objects.create(username='Прохожий')
        cls.auth_client = Client()
        cls.auth_client.force_login(cls.user)
        cls.note = Note.objects.create(
            title='Заголовок',
            text='Текст заметки',
            slug='note-slug',
            author=cls.author,
        )
        cls.args_slug = cls.note.slug,