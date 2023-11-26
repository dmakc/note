from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

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
        cls.notes = Note.objects.create(
            title='Заметка',
            text='Текст заметки',
            slug='not-slug',
            author=cls.author
        )
        cls.url = reverse('notes:add')
        cls.form_data = {
            'title': cls.NOTE_TEXT,
            'text': 'Текст заметки',
            'slug': 'not-slug',
        }

    def test_anonymous_user_cant_create_comment(self):
        self.client.post(self.url, data=self.form_data)
        comments_count = Note.objects.count()
        self.assertEqual(comments_count, 1)

    def test_user_can_create_comment(self):
        response = self.author_client.post(self.url, data=self.form_data)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        note_count = Note.objects.count()
        self.assertEqual(note_count, 1)
        note = Note.objects.get()
        self.assertEqual(note.title, self.NOTE_TEXT)

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


class TestNoteCreation1(TestCase):
    NOTE_TEXT = 'Заметка'

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Автор')
        cls.author_client = Client()
        cls.author_client.force_login(cls.author)
        cls.notes = Note.objects.create(
            title='Заметка',
            text='Текст заметки',
            author=cls.author
        )
        cls.url = reverse('notes:add')
        cls.form_data = {
            'title': cls.NOTE_TEXT,
            'text': 'Текст заметки',
        }

    def test_empty_slug(self):
        pass
