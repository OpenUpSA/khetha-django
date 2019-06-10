from django.contrib import admin
from django.urls import path
from django.views import generic

from khetha import views

urlpatterns: list = [
    # Transitional redirects:
    path("bigdebate/", generic.RedirectView.as_view(pattern_name="task-list")),
    path("bigdebatepoll/", generic.RedirectView.as_view(pattern_name="task-list")),
    path("intro/", generic.RedirectView.as_view(pattern_name="task-list")),
    path("progress/", generic.RedirectView.as_view(pattern_name="task-list")),
    path("start/", generic.RedirectView.as_view(pattern_name="task-list")),
    path("task/", generic.RedirectView.as_view(pattern_name="task-list")),
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
