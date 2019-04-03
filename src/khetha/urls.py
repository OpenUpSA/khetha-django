from django.contrib import admin
from django.urls import path
from django.views import generic

from khetha import views

urlpatterns: list = [
    path("", generic.RedirectView.as_view(pattern_name="task-list"), name="home"),
    path("tasks/", views.TaskListView.as_view(), name="task-list"),
    path("tasks/<slug:slug>/", views.TaskDetailView.as_view(), name="task-detail"),
    path("admin/", admin.site.urls),
]
