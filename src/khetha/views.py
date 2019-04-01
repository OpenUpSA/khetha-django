from django.views import generic

from khetha import models


class TaskListView(generic.ListView):
    queryset = models.Task.objects.filter(is_published=True)


class TaskDetailView(generic.DetailView):
    queryset = models.Task.objects.filter(is_published=True)
