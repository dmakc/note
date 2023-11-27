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


class TestCommentEditDelete(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Автор')
        cls.author_client = Client()
        cls.author_client.force_login(cls.author)
        cls.reader = User.objects.create(username='Читатель')
        cls.reader_client = Client()
        cls.reader_client.force_login(cls.reader)
        cls.notes = Note.objects.create(
            title='Заметка',
            text='Текст заметки',
            slug='not-slug',
            author=cls.author,
        )
        cls.form_data = {
            'title': 'Заметка',
            'text': 'Текст заметки',
        }
        cls.url = reverse('notes:edit', args=(cls.notes.slug,))
        cls.delete_url = reverse('notes:delete', args=(cls.notes.slug,))

    def test_author_can_edit_note(self):
        response = self.author_client.post(self.url, self.form_data)
        self.assertRedirects(response, reverse('notes:success'))
        note = Note.objects.get()
        self.assertEqual(note.title, self.form_data['title'])
        self.assertEqual(note.text, self.form_data['text'])

    def test_other_user_cant_edit_note(self):
        response = self.reader_client.post(self.url, self.form_data)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        note_from_db = Note.objects.get(id=self.notes.id)
        self.assertEqual(self.notes.title, note_from_db.title)
        self.assertEqual(self.notes.text, note_from_db.text)
        self.assertEqual(self.notes.slug, note_from_db.slug)

    def test_author_can_delete_note(self):
        response = self.author_client.delete(self.delete_url)
        self.assertRedirects(response, reverse('notes:success'))
        note_count = Note.objects.count()
        self.assertEqual(note_count, 0)

    def test_other_user_cant_delete_note(self):
        response = self.reader_client.delete(self.delete_url)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        note_count = Note.objects.count()
        self.assertEqual(note_count, 1)
