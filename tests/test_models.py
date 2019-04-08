from django.db.models.options import Options
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
    fixtures = ["sample-task-data"]

    def test_create(self) -> None:
        task = models.Task.objects.create()
        assert {
            "description": "",
            "id": task.pk,
            "is_published": False,
            "order": 0,
            "points": 0,
            "slug": "",
            "title": "",
        } == models.Task.objects.values().get(pk=task.pk)

    def test_str(self) -> None:
        assert "" == str(models.Task.objects.create())

    def test_get_absolute_url(self) -> None:
        task = models.Task.objects.create(slug="spam")
        assert "/tasks/spam/" == task.get_absolute_url()

    def test_questions(self) -> None:
        task: models.Task = models.Task.objects.get(slug="views-on-elections")
        self.assertQuerysetEqual(
            task.question_set.order_by("order"), task.questions(), transform=lambda o: o
        )


class TestQuestion(TestCase):
    fixtures = ["sample-task-data"]

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
            "order": 0,
            "task_id": question.task.pk,
            "text": "",
            "display_type": models.QuestionDisplayType.short_text.value,
        } == models.Question.objects.values().get(pk=question.pk)

    def test_str(self) -> None:
        assert "" == str(self._create())

    def test_answer_options(self) -> None:
        task: models.Task = models.Task.objects.get(slug="views-on-elections")
        for question in task.questions().filter(answeroption__isnull=False):
            assert 0 < question.answeroption_set.count()  # self-integrity check
            self.assertQuerysetEqual(
                question.answeroption_set.order_by("order"),
                question.answer_options(),
                transform=lambda o: o,
            )

    def test_display_type(self) -> None:
        assert isinstance(models.Question._meta, Options)
        field = models.Question._meta.get_field("display_type")
        assert [
            (1, "Short text"),
            (2, "Long text"),
            (3, "Buttons"),
            (4, "Select list"),
        ] == field.flatchoices  # type: ignore

    def test_display_type_enum(self) -> None:
        question = self._create()
        assert models.QuestionDisplayType.short_text is question.display_type_enum
        question.display_type_enum = models.QuestionDisplayType.long_text
        assert models.QuestionDisplayType.long_text.value == question.display_type


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
            "order": 0,
            "question_id": answer_option.question.pk,
            "text": "",
        } == models.AnswerOption.objects.values().get(pk=answer_option.pk)

    def test_str(self) -> None:
        assert "" == str(self._create())


class TestTaskSubmission(TestCase):

    fixtures = ["sample-task-data"]

    def test_answers(self) -> None:
        self.assertQuerysetEqual([], models.Answer.objects.all())
        for task in models.Task.objects.all():
            with self.subTest(task=task):
                tasksubmission = models.TaskSubmission.objects.create(
                    task=task, user_key="user-1"
                )
                assert list(task.questions()) == [
                    answer.question for answer in tasksubmission.answers()
                ]
        assert models.Question.objects.count() == models.Answer.objects.count()
