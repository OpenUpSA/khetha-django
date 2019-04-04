from functools import partial

from django.contrib.auth.models import AbstractUser
from django.db import models

# Field shortcuts:
_CharField = partial(models.CharField, max_length=1024)
_ForeignKey = partial(models.ForeignKey, on_delete=models.CASCADE)
# Blank fields:
_BlankTextField = partial(models.TextField, blank=True)


class User(AbstractUser):
    pass


class Task(models.Model):
    slug: str = models.SlugField()

    title: str = _CharField()
    description = _BlankTextField()
    points = models.PositiveSmallIntegerField(default=0)

    is_published = models.BooleanField(default=False)

    order = models.PositiveIntegerField(default=0)

    class Meta(object):
        ordering = ["order"]

    def __str__(self) -> str:
        return self.title

    def questions(self) -> models.QuerySet:
        """
        The questions to show for this task, in order.
        """
        return self.question_set.all()


class Question(models.Model):
    task = _ForeignKey(Task)

    text: str = _CharField()
    description = _BlankTextField()

    order = models.PositiveIntegerField(default=0)

    class Meta(object):
        ordering = ["order"]

    def __str__(self) -> str:
        return self.text

    def answer_options(self) -> models.QuerySet:
        """
        The answer options to show for this question, in order.
        """
        return self.answeroption_set.all()


class AnswerOption(models.Model):
    question = _ForeignKey(Question)

    text: str = _CharField()

    order = models.PositiveIntegerField(default=0)

    class Meta(object):
        ordering = ["order"]

    def __str__(self) -> str:
        return self.text
