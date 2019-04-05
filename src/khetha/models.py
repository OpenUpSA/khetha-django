from __future__ import annotations

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


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


class Question(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)

    text = models.CharField(max_length=1024)
    description = models.TextField(blank=True)

    order = models.PositiveIntegerField(default=0)

    class Meta(object):
        ordering = ["order"]

    def __str__(self) -> str:
        return self.text

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


class Answer(TimestampedModel):
    tasksubmission = models.ForeignKey(TaskSubmission, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    value = models.TextField(blank=True)

    def __str__(self) -> str:
        return self.value
