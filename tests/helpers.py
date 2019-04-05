from __future__ import annotations

from typing import cast

from django.http.response import HttpResponse
from django.template.context import Context
from django.test.utils import ContextList


class TestResponse(HttpResponse):
    """Helper to assert the response context in tests."""

    context: Context

    @staticmethod
    def check(response: HttpResponse) -> TestResponse:
        assert isinstance(response.context, (Context, ContextList))
        return cast(TestResponse, response)
