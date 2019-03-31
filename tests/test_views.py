from http import HTTPStatus

from django.http import HttpResponse
from django.test import TestCase
from django.urls import reverse

from khetha import models


class TestTaskListView(TestCase):
    fixtures = ["sample-task-data"]

    def _get(self) -> HttpResponse:
        response: HttpResponse = self.client.get(reverse("task-list"))
        self.assertTemplateUsed("khetha/task_list.html")
        assert HTTPStatus.OK == response.status_code
        return response

    def test_get__not_published(self) -> None:
        models.Task.objects.update(is_published=False)
        response = self._get()
        self.assertQuerysetEqual([], response.context["task_list"])

    def test_get__published(self) -> None:
        count = models.Task.objects.update(is_published=True)
        assert 0 < count  # Check test integrity

        response = self._get()
        expected_tasks = models.Task.objects.all()
        self.assertQuerysetEqual(
            expected_tasks,
            response.context["task_list"],
            transform=lambda o: o,
            ordered=False,
        )
        for task in expected_tasks:
            with self.subTest(task=task):
                self.assertContains(response, task.title)
