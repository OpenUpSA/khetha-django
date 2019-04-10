from http import HTTPStatus
from typing import List, Optional

from django.contrib import messages
from django.contrib.messages.storage.base import Message
from django.contrib.sessions.backends.base import SessionBase
from django.http.response import HttpResponse
from django.test import TestCase
from django.urls import reverse

from helpers import TestResponse
from khetha import models, views


def assert_messages(response: HttpResponse, expected_messages: List[str]) -> None:
    """
    Assert the given Django messages, as text (ignoring level and tags).
    """
    actual_messages: List[Message] = list(messages.get_messages(response.wsgi_request))
    actual_message_texts = [m.message for m in actual_messages]
    assert expected_messages == actual_message_texts, ()


# Test helpers:
# (Check the counts, for test integrity.)
def _publish_tasks() -> None:
    assert 0 < models.Task.objects.update(is_published=True)


def _unpublish_tasks() -> None:
    assert 0 < models.Task.objects.update(is_published=False)


class TestHome(TestCase):
    def test_get(self) -> None:
        response = self.client.get("/")
        self.assertRedirects(response, reverse("task-list"))


class TestTaskListView(TestCase):
    fixtures = ["sample-task-data"]

    def _get(self) -> TestResponse:
        response = TestResponse.check(self.client.get(reverse("task-list")))
        self.assertTemplateUsed("khetha/task_list.html")
        assert HTTPStatus.OK == response.status_code
        expected_user_key = views.get_user_key(response.wsgi_request)
        assert expected_user_key == response.context["user_key"]
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

    def _get(self, *, slug: str) -> TestResponse:
        return TestResponse.check(
            self.client.get(reverse("task-detail", kwargs={"slug": slug}))
        )

    def test_not_found(self) -> None:
        _unpublish_tasks()
        task: models.Task
        for task in models.Task.objects.all():
            response = self._get(slug=task.slug)
            assert HTTPStatus.NOT_FOUND == response.status_code
            self.assertTemplateNotUsed("khetha/task_detail.html")
            assert "task" not in response.context

    def _get_ok(self, task: models.Task) -> TestResponse:
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


class TestAnswerUpdateView(TestCase):
    fixtures = ["sample-task-data"]

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        cls._create_answers("test-user-1")
        cls._create_answers("test-user-2")

    @classmethod
    def _create_answers(cls, user_key: str) -> None:
        task: models.Task
        for task in models.Task.objects.all():
            tasksubmission: models.TaskSubmission = task.get_submission(user_key)
            assert 0 < len(tasksubmission.answers()) == task.questions().count()

    def setUp(self) -> None:
        super().setUp()
        self.answer = models.Answer.objects.filter(
            tasksubmission__user_key="test-user-1"
        ).earliest("created_at")
        self._set_user_key("test-user-1")

    def _set_user_key(self, user_key: str) -> None:
        # https://docs.djangoproject.com/en/stable/topics/testing/tools/#django.test.Client.session
        session: SessionBase = self.client.session
        session[views.SESSION_USER_KEY_NAME] = user_key
        session.save()

    def _get(self, *, pk: int) -> HttpResponse:
        path = reverse("answer-update", kwargs={"pk": pk})
        return self.client.get(path)

    def _post(self, *, pk: int, data: Optional[dict] = None) -> HttpResponse:
        path = reverse("answer-update", kwargs={"pk": pk})
        return self.client.post(path, data=data)

    def test_get__not_found(self) -> None:
        assert HTTPStatus.NOT_FOUND == self._get(pk=404).status_code

    def test_get_post__no_access(self) -> None:
        self._set_user_key("test-user-2")
        assert HTTPStatus.NOT_FOUND == self._get(pk=self.answer.pk).status_code
        assert HTTPStatus.NOT_FOUND == self._post(pk=self.answer.pk).status_code

    def test_get(self) -> None:
        task: models.Task = self.answer.tasksubmission.task
        response = self._get(pk=self.answer.pk)
        self.assertRedirects(response, task.get_absolute_url())

    def test_post__empty(self) -> None:
        task: models.Task = self.answer.tasksubmission.task
        response = self._post(pk=self.answer.pk, data={})
        self.assertRedirects(response, task.get_absolute_url())
        self.answer.refresh_from_db()
        assert "" == self.answer.value

    def test_post__values(self) -> None:
        task: models.Task = self.answer.tasksubmission.task
        for value in ["one", "two", "three"]:
            with self.subTest(value=value):
                response = self._post(pk=self.answer.pk, data={"value": value})
                self.assertRedirects(response, task.get_absolute_url())
                self.answer.refresh_from_db()
                assert value == self.answer.value
