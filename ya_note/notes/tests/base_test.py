from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from notes.models import Note

User = get_user_model()


class BaseTest(TestCase):

    AUTHOR = 'Марти Макфлай'
    READER = 'Морти Смит'
    ANONYMOUS = 'anonymous'
    SLUG = 'S'
    TITLE = 'Заголовок'
    TEXT = 'текст'
    NEW_SLUG = 'New-S'
    NEW_TITLE = 'Новый заголовок'
    NEW_TEXT = 'Новый текст'

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username=cls.AUTHOR)
        cls.author_client = Client()
        cls.author_client.force_login(cls.author)
        cls.reader = User.objects.create(username=cls.READER)
        cls.reader_client = Client()
        cls.reader_client.force_login(cls.reader)
        cls.notes = Note.objects.create(title=cls.TITLE,
                                        text=cls.TEXT, slug=cls.SLUG,
                                        author=cls.author)
        cls.form_data = {'text': cls.NEW_TEXT,
                         'title': cls.NEW_TITLE,
                         'slug': cls.NEW_SLUG}
        cls.url_add = reverse('notes:add')
        cls.url_success = reverse('notes:succes')
        cls.url_delete = reverse('notes:delete', args=(cls.SLUG,))
        cls.url_detail = reverse('notes:detail', args=(cls.SLUG,))
        cls.url_edit = reverse('notes:edit', args=(cls.SLUG,))
        cls.url_home = reverse('notes:home')
        cls.url_list = reverse('notes:list')
        cls.url_login = reverse('users:login')
        cls.url_logout = reverse('users:logout')
        cls.url_sign_up = reverse('users:signup')
        cls.url_succes = reverse('notes:success')
