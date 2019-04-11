from typing import Optional

from django import template
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from khetha import models

register = template.Library()


@register.filter_function
def get_submission(task: models.Task, user_key: str) -> models.TaskSubmission:
    """
    Expose `models.Task.get_submission`.
    """
    return task.get_submission(user_key)


@register.simple_tag
def google_maps_api_key() -> str:
    api_key: Optional[str] = getattr(settings, "GOOGLE_MAPS_API_KEY", None)
    if api_key:
        return api_key
    else:
        raise ImproperlyConfigured("settings.GOOGLE_MAPS_API_KEY not set")
