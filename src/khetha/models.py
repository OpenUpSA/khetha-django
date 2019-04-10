from __future__ import annotations

import enum
from typing import List, Tuple

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse

from django_missing_bits import missing_utils


class TimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    modified_at = models.DateTimeField(auto_now=True, db_index=True)

    class Meta:
        abstract = True


class User(AbstractUser):
    pass


class Task(models.Model):
    slug = models.SlugField()

    title = models.CharField(max_length=1024)
    description = models.TextField(blank=True)
    points = models.PositiveSmallIntegerField(default=0)

    is_published = models.BooleanField(default=False)

    order = models.PositiveIntegerField(default=0)

    class Meta(object):
        ordering = ["order"]

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self) -> str:
        return reverse("task-detail", kwargs={"slug": self.slug})

    def questions(self) -> models.QuerySet[Question]:
        """
        The questions to show for this task, in order.
        """
        return self.question_set.all()

    def get_submission(self, user_key: str) -> TaskSubmission:
        """
        Get (or create) the active task submission this task and user_key.
        """
        (tasksubmission, created) = self.tasksubmission_set.get_or_create(
            user_key=user_key
        )
        return tasksubmission


@enum.unique
class QuestionDisplayType(enum.Enum):
    """
    Ways to display different types of `Question` answers.

    See: `Question.display_type`

    Value convention: These use a decimal scheme for now, to have space to add
    related types without changing the value ordering.

    (Value 0 is not used, to avoid conflating with the default database value.)
    """

    short_text = 10
    long_text = 11
    buttons = 20
    select_list = 30
    radio_buttons = 40


class Question(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)

    # https://code.djangoproject.com/ticket/24342
    display_type = models.PositiveSmallIntegerField(
        db_index=True,
        default=QuestionDisplayType.short_text.value,
        choices=missing_utils.enum_choices(QuestionDisplayType),
    )

    text = models.CharField(max_length=1024)

    description = models.TextField(blank=True)

    order = models.PositiveIntegerField(default=0)

    class Meta(object):
        ordering = ["order"]

    def __str__(self) -> str:
        return self.text

    @property
    def display_type_enum(self) -> QuestionDisplayType:
        """
        Access `display_type` as an `Enum`.
        """
        return QuestionDisplayType(self.display_type)

    @display_type_enum.setter
    def display_type_enum(self, member: QuestionDisplayType) -> None:
        self.display_type = member.value

    def answer_options(self) -> models.QuerySet[AnswerOption]:
        """
        The answer options to show for this question, in order.
        """
        return self.answeroption_set.all()


class AnswerOption(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    text = models.CharField(max_length=1024)

    order = models.PositiveIntegerField(default=0)

    class Meta(object):
        ordering = ["order"]

    def __str__(self) -> str:
        return self.text


class TaskSubmission(TimestampedModel):
    # Key the submissions by task and an arbitrary user key, for now.
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    user_key = models.CharField(max_length=1024, db_index=True)

    def answers(self) -> List[Answer]:
        """
        Get or create the set of answers for this task submission.
        """
        answers_creations: List[Tuple[Answer, bool]] = [
            self.answer_set.get_or_create(question=question)
            for question in self.task.questions()
        ]
        return [answer for (answer, created) in answers_creations]

    def progress_factor(self) -> float:
        answered_count: int = self.answer_set.exclude(value="").count()
        question_count: int = self.task.questions().count()
        return answered_count / question_count

    def is_completed(self) -> bool:
        return self.progress_factor() == 1

    def get_task_url(self) -> str:
        """
        Get the URL for this submission's task.

        XXX: This adds a no-effect "completed" query parameter
        if this user's submission is completed.
        """
        task_url = self.task.get_absolute_url()
        return f"{task_url}?completed" if self.is_completed() else task_url


class Answer(TimestampedModel):
    tasksubmission = models.ForeignKey(TaskSubmission, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    value = models.TextField(blank=True)

    def __str__(self) -> str:
        return self.value
