from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from ..forms import TaskForm
from ..models import Task
from .login import check_project, check_dev


# Vistas del modelo Task.
class TaskCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = "project_task/task_create.html"

    def test_func(self):
        return check_project(self.request.user)

    success_url = reverse_lazy('projectman:list_task')


@login_required
def task_list_filter(request, pk):
    tareas = Task.objects.filter(project=pk)
    context = {'tareas': tareas}
    return render(request, 'project_task/task_list_filter.html', context)


class TaskList(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Task
    template_name = 'project_task/task_list.html'

    def test_func(self):
        dev = check_dev(self.request.user)
        prod = check_project(self.request.user)
        return prod or dev

    success_url = reverse_lazy('projectman:list_task')


class TaskUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'project_task/task_create.html'

    def test_func(self):
        dev = check_dev(self.request.user)
        prod = check_project(self.request.user)
        return prod or dev


class TaskDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Task
    template_name = 'project_task/task_delete.html'

    def test_func(self):
        return check_project(self.request.user)

    success_url = reverse_lazy('projectman:list_task')


class TaskDetail(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Task
    template_name = 'project_task/task_detail.html'

    def test_func(self):
        dev = check_dev(self.request.user)
        prod = check_project(self.request.user)
        return prod or dev
