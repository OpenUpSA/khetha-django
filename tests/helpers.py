from __future__ import annotations

from typing import cast

from django.http.response import HttpResponse
from django.template.context import Context


class TestResponse(HttpResponse):
    """Helper to assert the response context in tests."""

    context: Context

    @staticmethod
    def check(response: HttpResponse) -> TestResponse:
        response = cast(TestResponse, response)
        if response.context is None:
            response.context = {}
        return response
