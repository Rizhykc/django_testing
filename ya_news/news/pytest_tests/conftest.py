from datetime import timedelta

import pytest
from django.conf import settings
from django.urls import reverse
from django.utils import timezone
from pytest_lazyfixture import lazy_fixture

from news.models import Comment, News

ADMIN_CLIENT = lazy_fixture('admin_client')
AUTHOR_CLIENT = lazy_fixture('author_client')
ANONYMOUS = lazy_fixture('client')
NEWS = lazy_fixture('news')
NEWS_DETAIL = 'news:detail'
NEWS_HOME = 'news:home'
TITLE = 'Заголовок'
TEXT = 'Текст'
NEW_TEXT = 'Новый текст'
COMMENTS_COUNT = 3
COUNT_ADD = 1


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(
        username='Марти Макфлай',
        password='delorean'
    )


@pytest.fixture
def author_client(author, client):

    client.force_login(author)
    return client


@pytest.fixture
def reader(django_user_model):
    return django_user_model.objects.create(
        username='Морти Смит',
        password='Wubbalubbadubdub'
    )


@pytest.fixture
def reader_client(reader, client):

    client.force_login(reader)
    return client


@pytest.fixture
def new(author):

    news = News.objects.create(
        title=TITLE,
        text=TEXT,
    )
    return news


@pytest.fixture
def bulk_news_creation(author):

    return News.objects.bulk_create(
        News(
            title=f'{TITLE} {index}',
            text=TEXT,
        )
        for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
    )


@pytest.fixture
def comment(author, new):

    comment = Comment.objects.create(
        author=author,
        news=new,
        text=TEXT
    )
    return comment


@pytest.fixture
def multiply_comments(author, new):

    for index in range(5):
        comment = Comment.objects.create(
            author=author,
            news=new,
            text=f'{TEXT} {index}',
        )
        comment.created = timezone.now() + timedelta(days=index)
        comment.save()


@pytest.fixture
def new_comment():
    return {'text': NEW_TEXT}


@pytest.fixture
def home_url():
    return reverse('news:home')


@pytest.fixture
def detail_url(new):
    return reverse('news:detail', args=(new.id,))


@pytest.fixture
def delete_comment_url(comment):
    return reverse('news:delete', args=(comment.id,))


@pytest.fixture
def edit_comment_url(comment):
    return reverse('news:edit', args=(comment.id,))


@pytest.fixture
def login_url():
    return reverse('users:login')


@pytest.fixture
def logout_url():
    return reverse('users:logout')


@pytest.fixture
def signup_url():
    return reverse('users:signup')
