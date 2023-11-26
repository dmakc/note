# from http import HTTPStatus

# from django.contrib.auth import get_user_model
# from django.test import Client, TestCase
# from django.urls import reverse

# from notes.forms import WARNING
# from notes.models import Note

# User = get_user_model()


# class TestNoteCreation(TestCase):
#     NOTE_TEXT = 'Текст комментария'

#     @classmethod
#     def setUpTestData(cls):
#         cls.notes = Note.objects.create(
#             title='Заголовок',
#             text='Текст',
#             slug='not-slug',
#         )
#         cls.url = reverse('notes:detail', args=(cls.notes.slug,))
#         cls.user = User.objects.create(username='Автор')
#         cls.auth_client = Client()
#         cls.auth_client.force_login(cls.user)
#         cls.form_data = {'text': cls.NOTE_TEXT}

#     def test_anonymous_user_cant_create_comment(self):
#         self.client.post(self.url, data=self.form_data)
#         notes_count = Note.objects.count()
#         self.assertEqual(notes_count, 0)

#     # def test_user_can_create_comment(self):
#     #     response = self.auth_client.post(self.url, data=self.form_data)
#     #     self.assertRedirects(response, f'{self.url}#add')
#     #     notes_count = Note.objects.count()
#     #     self.assertEqual(notes_count, 1)
#     #     note = Note.objects.get()
#     #     self.assertEqual(note.text, self.NOTE_TEXT)
#     #     self.assertEqual(note.slug, self.notes)
#     #     self.assertEqual(note.author, self.user)


# # class TestCommentEditDelete(TestCase):
# #     NOTE_TEXT = 'Текст комментария'
# #     NEW_NOTE_TEXT = 'Обновлённый комментарий'

# #     @classmethod
# #     def setUpTestData(cls):
# #         cls.notes = Note.objects.create(title='Заголовок', text='Текст', slug='Zogolovok')
# #         # Формируем адрес блока с комментариями, который понадобится для тестов.
# #         notes_url = reverse('notes:detail', args=(cls.notes.slug,))  # Адрес новости.
# #         cls.url_to_notes = notes_url + '#id_title'  # Адрес блока с комментариями.
# #         # Создаём пользователя - автора комментария.
# #         cls.author = User.objects.create(username='Автор')
# #         # Создаём клиент для пользователя-автора.
# #         cls.author_client = Client()
# #         # "Логиним" пользователя в клиенте.
# #         cls.author_client.force_login(cls.author)
# #         # Делаем всё то же самое для пользователя-читателя.
# #         cls.reader = User.objects.create(username='Читатель')
# #         cls.reader_client = Client()
# #         cls.reader_client.force_login(cls.reader)
# #         # Создаём объект комментария.
# #         cls.addnotes = Note.objects.create(
# #             news=cls.notes,
# #             author=cls.author,
# #             text=cls.NOTE_TEXT
# #         )
# #         # URL для редактирования комментария.
# #         cls.edit_url = reverse('notes:edit', args=(cls.addnotes.slug,)) 
# #         # URL для удаления комментария.
# #         cls.delete_url = reverse('notes:delete', args=(cls.addnotes.slug,))  
# #         # Формируем данные для POST-запроса по обновлению комментария.
# #         cls.form_data = {'text': cls.NEW_NOTE_TEXT}

# #     def test_author_can_delete_comment(self):
# #         response = self.author_client.delete(self.delete_url)
# #         self.assertRedirects(response, self.url_to_notes)
# #         comments_count = Note.objects.count()
# #         self.assertEqual(comments_count, 0)
