from django.contrib.auth import get_user_model

from notes.forms import NoteForm
from notes.tests.base_test import BaseTest

User = get_user_model()


class TestContent(BaseTest):

    def test_notes_list_for_different_users(self):
        users_statuses = (
            (self.author_client, True),
            (self.reader_client, False),
        )
        for user, value in users_statuses:
            with self.subTest():
                response = user.get(self.url_list)
                object_list = response.context['object_list']
                self.assertIs((self.note in object_list), value)

    def test_create_and_add_note_pages_contains_form(self):
        urls = (
            (self.url_add),
            (self.url_edit)
        )
        for url in urls:
            with self.subTest(name=url):
                response = self.author_client.get(url)
                self.assertIn('form', response.context)
                self.assertIsInstance(response.context['form'], NoteForm)
