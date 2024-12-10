from http import HTTPStatus

from django.contrib.auth import get_user_model
from notes.tests.base_test import BaseTest

User = get_user_model()


class TestRoutes(BaseTest):

    def test_pages_availability(self):

        urls = (
            (self.url_home, self.client, HTTPStatus.OK, self.ANONYMOUS),
            (self.url_login, self.client, HTTPStatus.OK, self.ANONYMOUS),
            (self.url_logout, self.client, HTTPStatus.OK, self.ANONYMOUS),
            (self.url_sign_up, self.client, HTTPStatus.OK, self.ANONYMOUS),
            (self.url_detail, self.author_client, HTTPStatus.OK, self.AUTHOR),
            (
                self.url_edit,
                self.author_client,
                HTTPStatus.OK,
                self.AUTHOR,
            ),
            (
                self.url_delete,
                self.author_client,
                HTTPStatus.OK,
                self.AUTHOR,
            ),
            (
                self.url_add,
                self.reader_client,
                HTTPStatus.OK,
                self.READER,
            ),
            (
                self.url_success,
                self.reader_client,
                HTTPStatus.OK,
                self.READER,
            ),
            (self.url_list, self.reader_client, HTTPStatus.OK, self.READER),
            (
                self.url_detail,
                self.reader_client,
                HTTPStatus.NOT_FOUND,
                self.READER,
            ),
            (
                self.url_edit,
                self.reader_client,
                HTTPStatus.NOT_FOUND,
                self.READER,
            ),
            (
                self.url_delete,
                self.reader_client,
                HTTPStatus.NOT_FOUND,
                self.READER,
            ),
        )
        for current_url, current_client, status, user in urls:
            with self.subTest():
                self.assertEqual(
                    current_client.get(current_url).status_code, status
                )

    def test_redirects(self):

        urls = (
            self.url_add,
            self.url_success,
            self.url_detail,
            self.url_edit,
            self.url_delete,
            self.url_list,
        )
        for url in urls:
            with self.subTest():
                redirect_url = f'{self.url_login}?next={url}'
                response = self.client.get(url)
                self.assertRedirects(response, redirect_url)
