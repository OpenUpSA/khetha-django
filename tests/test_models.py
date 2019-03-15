from django.test import TestCase

from khetha import models


class TestUser(TestCase):
    def test_create(self) -> None:
        user = models.User.objects.create()
        assert {
            "date_joined": user.date_joined,
            "email": "",
            "first_name": "",
            "id": user.pk,
            "is_active": True,
            "is_staff": False,
            "is_superuser": False,
            "last_login": None,
            "last_name": "",
            "password": "",
            "username": "",
        } == models.User.objects.values().get(pk=user.pk)

    def test_str(self) -> None:
        assert "" == str(models.User.objects.create())
