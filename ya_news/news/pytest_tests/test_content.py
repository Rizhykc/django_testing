import pytest

from .conftest import ANONYMOUS, AUTHOR_CLIENT

pytestmark = [pytest.mark.django_db]


def test_news_count_order(client, home_url, bulk_news_creation):

    response = client.get(home_url)
    object_list = list(response.context['object_list'])
    assert object_list == sorted(
        object_list, key=lambda x: x.date, reverse=True
    )


def test_comments_order(client, detail_url, new, multiply_comments):

    response = client.get(detail_url)
    new = response.context['news']
    all_comments = list(new.comment_set.all())
    assert 'news' in response.context
    assert all_comments == sorted(all_comments, key=lambda x: x.created)


@pytest.mark.parametrize(
    'current_client, status',
    ((ANONYMOUS, False), (AUTHOR_CLIENT, True)),
)
def test_anonymous_has_no_form(
    current_client,
    detail_url,
    status,
    comment
):

    response = current_client.get(detail_url)
    assert ('form' in response.context) is status
