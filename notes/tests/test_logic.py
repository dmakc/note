from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from notes.forms import WARNING
from notes.models import Note

User = get_user_model()


class TestNoteCreation(TestCase):
    NOTE_TEXT = 'Текст комментария'

    @classmethod
    def setUpTestData(cls):
        cls.note = Note.objects.create(
            title='Заголовок',
            text='Текст',
            slug='not-slug',
        )
        cls.url = reverse('notes:detail', args=(cls.note.slug,))
        cls.user = User.objects.create(username='Автор')
        cls.auth_client = Client()
        cls.auth_client.force_login(cls.user)
        cls.form_data = {'text': cls.NOTE_TEXT}

    def test_anonymous_user_cant_create_comment(self):
        self.client.post(self.url, data=self.form_data)
        comments_count = Note.objects.count()
        self.assertEqual(comments_count, 0)

    def test_user_can_create_comment(self):
        response = self.auth_client.post(self.url, data=self.form_data)
        self.assertRedirects(response, f'{self.url}#detail')
        comments_count = Note.objects.count()
        self.assertEqual(comments_count, 1)
        comment = Note.objects.get()
        self.assertEqual(comment.text, self.NOTE_TEXT)
        self.assertEqual(comment.note, self.note)
        self.assertEqual(comment.author, self.user)
