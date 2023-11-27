from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from pytils.translit import slugify

from notes.forms import WARNING
from notes.models import Note

User = get_user_model()


class TestNoteCreation(TestCase):
    NOTE_TEXT = 'Заметка'

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Автор')
        cls.author_client = Client()
        cls.author_client.force_login(cls.author)
        cls.url = reverse('notes:add')
        cls.form_data = {
            'title': cls.NOTE_TEXT,
            'text': 'Текст заметки',
            'slug': 'not-slug',
        }

    def test_anonymous_user_cant_create_comment(self):
        response = self.client.post(self.url, data=self.form_data)
        login_url = reverse('users:login')
        expected_url = f'{login_url}?next={self.url}'
        self.assertRedirects(response, expected_url)
        comments_count = Note.objects.count()
        self.assertEqual(comments_count, 0)

    def test_user_can_create_comment(self):
        response = self.author_client.post(self.url, data=self.form_data)
        self.assertRedirects(response, reverse('notes:success'))
        note_count = Note.objects.count()
        self.assertEqual(note_count, 1)
        note = Note.objects.get()
        self.assertEqual(note.title, self.NOTE_TEXT)
        self.assertEqual(note.text, self.form_data['text'])
        self.assertEqual(note.slug, self.form_data['slug'])


class TestNoteUniqueSlug(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Автор')
        cls.author_client = Client()
        cls.author_client.force_login(cls.author)
        cls.notes = Note.objects.create(
            title='Заметка',
            text='Текст заметки',
            slug='not-slug',
            author=cls.author,
        )
        cls.url = reverse('notes:add')

    def test_not_unique_slug(self):
        bad_words_data = {'slug': f'{self.notes.slug}'}
        response = self.author_client.post(self.url, data=bad_words_data)
        self.assertFormError(
            response,
            form='form',
            field='slug',
            errors=(self.notes.slug + WARNING),
        )
        note_count = Note.objects.count()
        self.assertEqual(note_count, 1)


class TestNoteEmptySlug(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Автор')
        cls.author_client = Client()
        cls.author_client.force_login(cls.author)
        cls.url = reverse('notes:add')
        cls.form_data = {
            'title': 'Заметка',
            'text': 'Текст заметки',
        }

    def test_empty_slug(self):
        response = self.author_client.post(self.url, data=self.form_data)
        self.assertRedirects(response, reverse('notes:success'))
        note_count = Note.objects.count()
        self.assertEqual(note_count, 1)
        new_note = Note.objects.get()
        expected_slug = slugify(self.form_data['title'])
        self.assertEqual(new_note.slug, expected_slug)


# class TestCommentEditDelete(TestCase):

#     @classmethod
#     def setUpTestData(cls):
#         cls.author = User.objects.create(username='Автор')
#         cls.author_client = Client()
#         cls.author_client.force_login(cls.author)
#         cls.reader = User.objects.create(username='Читатель')
#         cls.reader_client = Client()
#         cls.reader_client.force_login(cls.reader)
#         cls.notes = Note.objects.create(
#             title='Заметка',
#             text='Текст заметки',
#             slug='not-slug',
#             author=cls.author,
#         )
#         cls.form_data = {
#             'title': 'Заметка',
#             'text': 'Текст заметки',
#         }
#         cls.url = reverse('notes:edit', args=(cls.notes.slug,))

#     def test_author_can_edit_note(self):
#         response = self.author_client.post(self.url, self.form_data)
#         self.assertRedirects(response, reverse('notes:success'))
#         note = Note.objects.get()
#         self.assertEqual(note.title, self.form_data['title'])
#         self.assertEqual(note.text, self.form_data['text'])

#     def test_other_user_cant_edit_note(self):
#         response = self.reader_client.post(self.url, self.form_data)
#         self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
#         note_from_db = Note.objects.get(id=self.notes.id)
#         self.assertEqual(self.notes.title, note_from_db.title)
#         self.assertEqual(self.notes.text, note_from_db.text)
#         self.assertEqual(self.notes.slug, note_from_db.slug)

#     def test_author_can_delete_note(self):
#         # url = reverse('notes:delete', args=self.notes.slug)
#         response = self.author_client.post(self.url)
#         self.assertRedirects(response, reverse('notes:success'))
#         note_count = Note.objects.count()
#         self.assertEqual(note_count, 1)


#     def test_other_user_cant_delete_note(admin_client, form_data, slug_for_args):
#         url = reverse('notes:delete', args=slug_for_args)
#         response = admin_client.post(url)
#         assert response.status_code == HTTPStatus.NOT_FOUND
#         assert Note.objects.count() == 1

class TestCommentEditDelete(TestCase):
    NOTE_TEXT = 'Текст заметки'
    NEW_NOTE_TEXT = 'Обновлённая заметка'

    @classmethod
    def setUpTestData(cls):
        cls.note = Note.objects.create(
            title='Заголовок',
            text='Текст',
        )
        news_url = reverse('news:edit', args=(cls.note.slug,))  # Адрес новости.
        cls.url_to_comments = news_url + '#comments'  # Адрес блока с комментариями.
        # Создаём пользователя - автора комментария.
        cls.author = User.objects.create(username='Автор комментария')
        # Создаём клиент для пользователя-автора.
        cls.author_client = Client()
        # "Логиним" пользователя в клиенте.
        cls.author_client.force_login(cls.author)
        # Делаем всё то же самое для пользователя-читателя.
        cls.reader = User.objects.create(username='Читатель')
        cls.reader_client = Client()
        cls.reader_client.force_login(cls.reader)
        # Создаём объект комментария.
        cls.new_note = Note.objects.create(
            news=cls.note,
            author=cls.author,
            text=cls.NOTE_TEXT
        )
        # URL для редактирования комментария.
        cls.edit_url = reverse('news:edit', args=(cls.new_note.id,))
        # URL для удаления комментария.
        cls.delete_url = reverse('news:delete', args=(cls.new_note.id,))
        # Формируем данные для POST-запроса по обновлению комментария.
        cls.form_data = {'text': cls.NEW_NOTE_TEXT}

    def test_author_can_delete_comment(self):
        # От имени автора комментария отправляем DELETE-запрос на удаление.
        response = self.author_client.delete(self.delete_url)
        # Проверяем, что редирект привёл к разделу с комментариями.
        # Заодно проверим статус-коды ответов.
        self.assertRedirects(response, self.url_to_comments)
        # Считаем количество комментариев в системе.
        comments_count = Note.objects.count()
        # Ожидаем ноль комментариев в системе.
        self.assertEqual(comments_count, 0)

    # def test_user_cant_delete_comment_of_another_user(self):
    #     # Выполняем запрос на удаление от пользователя-читателя.
    #     response = self.reader_client.delete(self.delete_url)
    #     # Проверяем, что вернулась 404 ошибка.
    #     self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
    #     # Убедимся, что комментарий по-прежнему на месте.
    #     comments_count = Comment.objects.count()
    #     self.assertEqual(comments_count, 1)

    # def test_author_can_edit_comment(self):
    #     # Выполняем запрос на редактирование от имени автора комментария.
    #     response = self.author_client.post(self.edit_url, data=self.form_data)
    #     # Проверяем, что сработал редирект.
    #     self.assertRedirects(response, self.url_to_comments)
    #     # Обновляем объект комментария.
    #     self.comment.refresh_from_db()
    #     # Проверяем, что текст комментария соответствует обновленному.
    #     self.assertEqual(self.comment.text, self.NEW_COMMENT_TEXT)

    # def test_user_cant_edit_comment_of_another_user(self):
    #     # Выполняем запрос на редактирование от имени другого пользователя.
    #     response = self.reader_client.post(self.edit_url, data=self.form_data)
    #     # Проверяем, что вернулась 404 ошибка.
    #     self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
    #     # Обновляем объект комментария.
    #     self.comment.refresh_from_db()
    #     # Проверяем, что текст остался тем же, что и был.
    #     self.assertEqual(self.comment.text, self.COMMENT_TEXT)