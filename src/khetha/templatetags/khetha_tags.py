from django import template

from khetha import models

register = template.Library()


@register.filter_function
def get_submission(task: models.Task, user_key: str) -> models.TaskSubmission:
    """
    Expose `models.Task.get_submission`.
    """
    return task.get_submission(user_key)
