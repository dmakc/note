# from django.conf import settings
# from django.contrib.auth import get_user_model
# from django.test import TestCase
# from django.urls import reverse
# from pytils.translit import slugify

# from notes.models import Note

# User = get_user_model()


# class TestDetailPage(TestCase):

#     @classmethod
#     def setUpTestData(cls):
#         cls.note = Note.objects.create(
#             title='Тестовая новость',
#             text='Просто текст.',
#             slug=slugify('title'),
#         )
#         cls.detail_url = reverse('notes:detail', args=(cls.note.slug,))
#         cls.author = User.objects.create(username='Комментатор')
#         for index in range(2):
#             note = Note.objects.create(
#                 news=cls.note, author=cls.author, text=f'Tекст {index}',
#             )
#             note.save()

#     def test_notes_order(self):
#         response = self.client.get(self.detail_url)
#         self.assertIn('note', response.context)
#         news = response.context['note']
#         all_notes = news.note_set.all()
#         self.assertLess(all_notes[0].created, all_notes[1].created)


#     def test_authorized_client_has_form(self):
#         self.client.force_login(self.author)
#         response = self.client.get(self.detail_url)
#         self.assertIn('form', response.context)
