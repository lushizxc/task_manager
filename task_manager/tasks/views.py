from django.db.migrations.operations import models
from django.shortcuts import render,get_object_or_404,redirect
from .models import Task
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from .forms import TaskForm
from django.urls import reverse_lazy
from django.views import View

class TaskListView(ListView):
    model = Task
    context_object_name = 'tasks'
    template_name = 'task_list.html'

    PRIORITY_FILTER_MAP = {
        'high': ['high', 'mid', 'low'],
        'mid': ['mid', 'low'],
        'low': ['low'],
    }

    def get_queryset(self):
        queryset = Task.objects.all().exclude(status='done')
        priority_filter = self.request.GET.get('priority_filter')

        if priority_filter:
            priorities_to_show = self.PRIORITY_FILTER_MAP.get(priority_filter)

            if priorities_to_show:
                queryset = queryset.filter(priority__in=priorities_to_show)

        return queryset

class TaskDetailView(DetailView):
    model = Task
    context_object_name = 'task'
    template_name  = 'task_detail.html'

class TaskCreateView(CreateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy('tasks:task_list')
    template_name = 'task_create.html'

class TaskUpdateView(UpdateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy('tasks:task_list')
    template_name = 'task_create.html'

class TaskDeleteView(DeleteView):
    model = Task
    success_url = reverse_lazy('tasks:task_list')
    template_name = 'task_delete.html'

class CompleteTaskView(View):
    def post(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        task.status = 'done'
        task.save()
        return redirect ('tasks:task_list')
