from __future__ import annotations

import uuid
from typing import Any, Dict

from django import forms
from django.contrib import messages
from django.contrib.sessions.backends.base import SessionBase
from django.core.handlers.wsgi import WSGIRequest
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.utils.html import format_html
from django.views import generic
from django.views.generic.edit import BaseUpdateView, FormMixin

from khetha import models

SESSION_USER_KEY_NAME = "khetha_user_key"


def get_user_key(request: HttpRequest) -> str:
    """
    Look up or initialise a user_key in the session.
    """
    session: SessionBase = request.session
    if SESSION_USER_KEY_NAME not in session:
        new_user_key: str = uuid.uuid4().hex
        session[SESSION_USER_KEY_NAME] = new_user_key
    user_key: str = session[SESSION_USER_KEY_NAME]
    return user_key


class TaskListView(generic.ListView):
    queryset = models.Task.objects.filter(is_published=True)

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        """
        Include the user's `user_key`.
        """
        user_key = get_user_key(self.request)
        return super().get_context_data(user_key=user_key, **kwargs)


class TaskDetailView(generic.DetailView):

    queryset = models.Task.objects.filter(is_published=True)

    object: models.Task

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        """
        Show the user's active submission for this task, if any.
        """
        user_key = get_user_key(self.request)
        return super().get_context_data(
            tasksubmission=self.object.get_submission(user_key), **kwargs
        )


class DjangoMessageErrorsFormMixin(FormMixin):
    """
    Show form errors as Django messages.

    This is intended for consumption by the MDC Snackbar.
    """

    def form_invalid(self, form: forms.BaseForm) -> HttpResponse:
        # The MDC Snackbar used for message display strips HTML from the label,
        # so just flatten this to plain text for now.
        message = format_html(
            "{} {}", form.errors.as_text(), form.non_field_errors().as_text()
        )
        assert isinstance(self.request, WSGIRequest), self.request
        messages.add_message(self.request, messages.ERROR, message)
        return super().form_invalid(form)


# Extend BaseUpdateView instead of UpdateView: we won't use templating.
class AnswerUpdateView(DjangoMessageErrorsFormMixin, BaseUpdateView):

    model = models.Answer
    fields = ["value"]

    object: models.Answer

    def get_queryset(self) -> QuerySet[models.Answer]:
        """
        Limit the editable answers to the user's session, or none.
        """
        user_key = get_user_key(self.request)
        queryset: QuerySet[models.Answer] = super().get_queryset()
        return queryset.filter(tasksubmission__user_key=user_key)

    # Redirect back to the task on success and otherwise:

    def get_success_url(self) -> str:
        task: models.Task = self.object.tasksubmission.task
        return task.get_absolute_url()

    def render_to_response(
        self, context: Dict[str, Any], **response_kwargs: Any
    ) -> HttpResponse:
        return HttpResponseRedirect(self.get_success_url())
