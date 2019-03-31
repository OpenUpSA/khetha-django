from django.contrib import admin
from django.urls import path

from khetha import views

urlpatterns: list = [
    path("", views.TaskListView.as_view(), name="task-list"),
    path("admin/", admin.site.urls),
]
