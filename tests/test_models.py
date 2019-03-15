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


class TestTask(TestCase):
    def test_create(self) -> None:
        task = models.Task.objects.create()
        assert {
            "description": "",
            "id": task.pk,
            "is_published": False,
            "points": 0,
            "slug": "",
            "title": "",
        } == models.Task.objects.values().get(pk=task.pk)

    def test_str(self) -> None:
        assert "" == str(models.Task.objects.create())


class TestQuestion(TestCase):
    @staticmethod
    def _create() -> models.Question:
        task: models.Task = models.Task.objects.create()
        question: models.Question = task.question_set.create()
        return question

    def test_create(self) -> None:
        question = self._create()
        assert {
            "description": "",
            "id": question.pk,
            "task_id": question.task.pk,
            "text": "",
        } == models.Question.objects.values().get(pk=question.pk)

    def test_str(self) -> None:
        assert "" == str(self._create())


class TestAnswerOption(TestCase):
    @staticmethod
    def _create() -> models.AnswerOption:
        question: models.Question = TestQuestion._create()
        answer_option: models.AnswerOption = question.answeroption_set.create()
        return answer_option

    def test_create(self) -> None:
        answer_option = self._create()
        assert {
            "id": answer_option.pk,
            "question_id": answer_option.question.pk,
            "text": "",
        } == models.AnswerOption.objects.values().get(pk=answer_option.pk)

    def test_str(self) -> None:
        assert "" == str(self._create())
