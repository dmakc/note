from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from notes.models import Note

User = get_user_model()


class TestContent(TestCase):
    LIST_URL = reverse('notes:list')

    @classmethod
    def setUpTestData(cls):
        author = User.objects.create(username='Автор')
        cls.author = Client()
        cls.author.force_login(author)
        reader = User.objects.create(username='Читатель')
        cls.reader = Client()
        cls.reader.force_login(reader)
        all_notes = [
            Note(
                title=f'Заголовок {index}',
                text='Текст заметки',
                slug=f'{index}',
                author=author,
            )
            for index in range(settings.NOTE_COUNT_ON_LIST_PAGE)
        ]
        cls.note = Note.objects.bulk_create(all_notes)

    def test_note_not_in_list_for_another_user(self):
        response = self.author.get(self.LIST_URL)
        object_list = response.context['object_list']
        notes_count = len(object_list)
        self.assertEqual(notes_count, settings.NOTE_COUNT_ON_LIST_PAGE)

    def test_notes_list_for_different_users(self):
        response = self.reader.get(self.LIST_URL)
        object_list = response.context['object_list']
        notes_count = len(object_list)
        self.assertNotEqual(notes_count, settings.NOTE_COUNT_ON_LIST_PAGE)


class TestFormPage(TestCase):

    @classmethod
    def setUpTestData(cls):
        author = User.objects.create(username='Автор')
        cls.author = Client()
        cls.author.force_login(author)
        cls.note = Note.objects.create(
            title='Заголовок',
            text='Текст заметки',
            slug='not-slug',
            author=author
        )

    def test_create_note_page_contains_form(self):
        url = reverse('notes:add')
        response = self.author.get(url)
        self.assertIn('form', response.context)

    def test_edit_note_page_contains_form(self):
        edit_url = reverse('notes:edit', args=(self.note.slug,))
        response = self.author.get(edit_url)
        self.assertIn('form', response.context)
