from http import HTTPStatus

from django.test import TestCase


class TestSmoke(TestCase):
    def test_root(self) -> None:
        response = self.client.get("/")
        assert HTTPStatus.OK == response.status_code
