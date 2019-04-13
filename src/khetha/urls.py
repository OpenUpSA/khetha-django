from textwrap import dedent
from typing import Any

from django.contrib import admin
from django.http import HttpRequest, HttpResponse
from django.urls import path
from django.views import generic
from django.views.generic.base import View

from khetha import views


class UnregisterServiceWorkerView(View):
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        # https://github.com/NekR/self-destroying-sw
        content = dedent(
            """\
            self.addEventListener('install', function(e) {
              self.skipWaiting();
            });
            self.addEventListener('activate', function(e) {
              self.registration.unregister()
                .then(function() {
                  return self.clients.matchAll();
                })
                .then(function(clients) {
                  clients.forEach(client => client.navigate(client.url))
                });
            });
            """
        )
        return HttpResponse(content=content, content_type="application/javascript")


urlpatterns: list = [
    path("sw.js", UnregisterServiceWorkerView.as_view()),
    # Khetha:
    path("", generic.RedirectView.as_view(pattern_name="task-list"), name="home"),
    path("tasks/", views.TaskListView.as_view(), name="task-list"),
    path(
        "tasks/completed/",
        views.TaskCompletedListView.as_view(),
        name="task-completed-list",
    ),
    path("tasks/<slug:slug>/", views.TaskDetailView.as_view(), name="task-detail"),
    # Django admin:
    path(
        "answers/<int:pk>/update/",
        views.AnswerUpdateView.as_view(),
        name="answer-update",
    ),
    path("admin/", admin.site.urls),
]
