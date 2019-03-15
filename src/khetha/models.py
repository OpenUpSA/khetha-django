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

    def __str__(self) -> str:
        return self.title


class Question(models.Model):
    task = _ForeignKey(Task)

    text: str = _CharField()
    description = _BlankTextField()

    def __str__(self) -> str:
        return self.text


class AnswerOption(models.Model):
    question = _ForeignKey(Question)

    text: str = _CharField()

    def __str__(self) -> str:
        return self.text
