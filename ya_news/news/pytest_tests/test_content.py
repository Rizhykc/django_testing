import pytest

from .conftest import ANONYMOUS, AUTHOR_CLIENT

pytestmark = [pytest.mark.django_db]


def test_news_count_order(client, home_url, bulk_news_creation):

    response = client.get(home_url)
    object_list = list(response.context['object_list'])
    assert object_list == sorted(
        object_list, key=lambda x: x.date, reverse=True
    )


def test_comments_order(self, client, detail_url, news, multiple_comments):

    response = client.get(detail_url)
    self.assertIn('news', response.context)
    comments = news.comment_set.order_by('created')
    for i in range(len(comments) - 1):
        self.assertLessEqual(
            comments[i].created,
            comments[i + 1].created
        )


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
