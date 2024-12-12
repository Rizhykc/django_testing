from http import HTTPStatus as HTTP

import pytest
from django.urls import reverse
from pytest_django.asserts import assertRedirects
from pytest_lazyfixture import lazy_fixture as lf

from .conftest import ADMIN_CLIENT, ANONYMOUS, AUTHOR_CLIENT


@pytest.mark.parametrize(
    'url, current_client, status', (
        (lf('home_url'), ANONYMOUS, HTTP.OK),
        (lf('detail_url'), ANONYMOUS, HTTP.OK),
        (lf('login_url'), ANONYMOUS, HTTP.OK),
        (lf('logout_url'), ANONYMOUS, HTTP.OK),
        (lf('signup_url'), ANONYMOUS, HTTP.OK),
        (lf('delete_comment_url'), AUTHOR_CLIENT, HTTP.OK),
        (lf('edit_comment_url'), AUTHOR_CLIENT, HTTP.OK),
        (lf('delete_comment_url'), ADMIN_CLIENT, HTTP.NOT_FOUND),
        (lf('edit_comment_url'), ADMIN_CLIENT, HTTP.NOT_FOUND),
    )
)
def test_pages_availability_for_users(url, current_client, status):

    response = current_client.get(url)
    assert response.status_code == status


@pytest.mark.parametrize('parametrized_client, expected_status', (
    (ADMIN_CLIENT, HTTP.NOT_FOUND),
    (AUTHOR_CLIENT, HTTP.OK)
),)
@pytest.mark.parametrize('name', ('news:edit', 'news:delete'),)
def test_availability_comments_edit_and_delete(
        parametrized_client, name, comment, expected_status
):

    url = reverse(name, args=(comment.id,))
    response = parametrized_client.get(url)
    assert response.status_code == expected_status


@pytest.mark.parametrize(
    'name',
    ('news:edit', 'news:delete'),
)
def test_redirects(client, name, comment):

    login_url = reverse('users:login')
    url = reverse(name, args=(comment.id,))
    expected_url = f'{login_url}?next={url}'
    response = client.get(url)
    assertRedirects(response, expected_url)
