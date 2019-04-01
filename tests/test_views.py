from http import HTTPStatus

from django.http import HttpResponse
from django.test import TestCase
from django.urls import reverse

from khetha import models

# Test helpers:
# (Check the counts, for test integrity.)


def _publish_tasks() -> None:
    assert 0 < models.Task.objects.update(is_published=True)


def _unpublish_tasks() -> None:
    assert 0 < models.Task.objects.update(is_published=False)


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
        _publish_tasks()
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


class TestTaskDetailView(TestCase):
    fixtures = ["sample-task-data"]

    def _get(self, *, slug: str) -> HttpResponse:
        return self.client.get(reverse("task-detail", kwargs={"slug": slug}))

    def test_not_found(self) -> None:
        _unpublish_tasks()
        task: models.Task = models.Task.objects.first()
        response = self._get(slug=task.slug)
        assert HTTPStatus.NOT_FOUND == response.status_code
        self.assertTemplateNotUsed("khetha/task_detail.html")
        assert "task" not in response.context

    def _get_ok(self, task: models.Task) -> HttpResponse:
        response = self._get(slug=task.slug)
        assert HTTPStatus.OK == response.status_code
        self.assertTemplateUsed("khetha/task_detail.html")
        assert task == response.context["task"]
        self.assertContains(response, task.title, count=1)
        for question in task.question_set.all():
            self.assertContains(response, question.text, count=1)
        return response

    def test_get__published(self) -> None:
        _publish_tasks()
        for task in models.Task.objects.all():
            with self.subTest(task=task):
                self._get_ok(task)
