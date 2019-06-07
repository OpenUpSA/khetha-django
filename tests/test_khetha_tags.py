from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.test import override_settings
from django.test.testcases import SimpleTestCase

from khetha.templatetags import khetha_tags


class Test_google_maps_api_key(SimpleTestCase):
    def test_missing(self) -> None:
        with override_settings(GOOGLE_MAPS_API_KEY=None):
            del settings.GOOGLE_MAPS_API_KEY
            with self.assertRaises(ImproperlyConfigured):
                khetha_tags.google_maps_api_key()

    def test_empty(self) -> None:
        for value in [None, ""]:
            with self.subTest(value=value):
                with override_settings(GOOGLE_MAPS_API_KEY=value):
                    with self.assertRaises(ImproperlyConfigured):
                        khetha_tags.google_maps_api_key()

    def test__configured(self) -> None:
        with override_settings(GOOGLE_MAPS_API_KEY="dummy-api-key"):
            assert "dummy-api-key" == khetha_tags.google_maps_api_key()
