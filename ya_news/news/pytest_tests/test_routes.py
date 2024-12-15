from http import HTTPStatus as HTTPs

import pytest
from django.urls import reverse
from pytest_django.asserts import assertRedirects
from pytest_lazyfixture import lazy_fixture as lf

from .conftest import ADMIN_CLIENT, ANONYMOUS, AUTHOR_CLIENT


@pytest.mark.parametrize(
    'url, current_client, status', (
        (lf('home_url'), ANONYMOUS, HTTPs.OK),
        (lf('detail_url'), ANONYMOUS, HTTPs.OK),
        (lf('login_url'), ANONYMOUS, HTTPs.OK),
        (lf('logout_url'), ANONYMOUS, HTTPs.OK),
        (lf('signup_url'), ANONYMOUS, HTTPs.OK),
        (None, AUTHOR_CLIENT, HTTPs.OK),
        (None, AUTHOR_CLIENT, HTTPs.OK),
        (None, ADMIN_CLIENT, HTTPs.NOT_FOUND),
        (None, ADMIN_CLIENT, HTTPs.NOT_FOUND),
    )
)
def test_pages_availability_for_users(url, current_client, status, comment):
    if url is None:
        comment_id = comment.id
        url = reverse(f'news:{"edit" if status == HTTPs.OK else "delete"}',
                      args=(comment_id,))
    response = current_client.get(url)
    assert response.status_code == status


@pytest.mark.parametrize(
    'url',
    [
        'news:edit',
        'news:delete',
    ]
)
def test_redirects(client, url, comment, login_url):

    login = login_url
    url = reverse(url, args=(comment.id,))
    expected_url = f'{login}?next={url}'
    response = client.get(url)
    assertRedirects(response, expected_url)
