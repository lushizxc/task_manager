from django.shortcuts import render,get_object_or_404,redirect
from .models import Task,Comment
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from .forms import TaskForm,CommentForm
from django.urls import reverse_lazy
from django.views import View
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin

class TaskListView(ListView,LoginRequiredMixin):
    model = Task
    context_object_name = 'tasks'
    template_name = 'task_list.html'
    paginate_by = 5

    PRIORITY_FILTER_MAP = {
        'high': ['high'],
        'mid': ['mid'],
        'low': ['low'],
    }

    def get_queryset(self):
        queryset = Task.objects.filter(creator=self.request.user).exclude(status='done')
        priority_filter = self.request.GET.get('priority_filter')
        search = self.request.GET.get('search')

        if search:
            queryset = queryset.filter(title__icontains=search)

        if priority_filter:
            priorities_to_show = self.PRIORITY_FILTER_MAP.get(priority_filter)

            if priorities_to_show:
                queryset = queryset.filter(priority__in=priorities_to_show)

        return queryset

class TaskDetailView(DetailView):
    model = Task
    context_object_name = 'task'
    template_name  = 'task_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        edit_comment_id =  self.request.GET.get('edit_comment')

        if edit_comment_id and edit_comment_id.isdigit():
            context['edit_comment_id'] = int(edit_comment_id)
        else:
            context['edit_comment_id'] = None

        return context


class TaskCreateView(CreateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy('tasks:task_list')
    template_name = 'task_create.html'

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Добавить задачу'
        context['button_text'] = 'Создать'
        return context

class TaskUpdateView(UpdateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy('tasks:task_list')
    template_name = 'task_create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Редактировать задачу'
        context['button_text'] = 'Сохранить'
        return context

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

class SingUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('tasks:task_list')
    template_name = 'signup.html'


class CompletedTaskListView(ListView,LoginRequiredMixin):
    model = Task
    context_object_name = 'tasks'
    template_name = 'task_list.html'
    paginate_by = 5

    def get_queryset(self):
        return Task.objects.filter(creator=self.request.user,status='done')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = "Архив выполненых задач"
        context['is_archived'] = True
        return context

class CommentCreationView(LoginRequiredMixin,View):
    def post(self,request,pk):
        task = get_object_or_404(Task, pk=pk)
        form = CommentForm(request.POST,request.FILES)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.task = task
            comment.author = request.user
            comment.save()
        return redirect('tasks:task_detail',pk=pk)

class CommentDeleteView(LoginRequiredMixin,DeleteView):
    model = Comment
    template_name = 'comment_delete.html'

    def get_queryset(self):
        return super().get_queryset().filter(author=self.request.user)

    def get_success_url(self):
        return reverse_lazy('tasks:task_detail',kwargs={'pk':self.object.task.pk})

class CommentUpdateView(LoginRequiredMixin,UpdateView):
    model = Comment
    fields = ['text']
    template_name = 'task_detail.html'

    def get_queryset(self):
        return super().get_queryset().filter(author=self.request.user)

    def get_success_url(self):
        return reverse_lazy('tasks:task_detail',kwargs={'pk':self.object.task.pk})