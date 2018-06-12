import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.core import serializers
from ..forms import TaskForm, CTaskRegisterForm
from ..models import Task, ChildTask
from .login import check_project, check_dev


# Vistas del modelo Task.
class TaskCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = "project_task/task_create.html"
    success_url = reverse_lazy('projectman:list_task')

    def test_func(self):
        return check_project(self.request.user)

    def form_valid(self, form):
        valid = super(TaskCreate, self).form_valid(form)
        task = self.object
        childs = form.cleaned_data.get('child_task').split('\r\n')
        for child in childs:
            ChildTask.objects.create(name=child, task=task).save()
        return valid


@login_required
def tasks_json(request):
    datos = [task.json for task in Task.objects.all()]
    return HttpResponse(json.dumps(datos), content_type='application/json')


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
    success_url = reverse_lazy('projectman:list_task')

    def test_func(self):
        dev = check_dev(self.request.user)
        prod = check_project(self.request.user)
        return prod or dev

    def form_valid(self, form):
        valid = super(TaskUpdate, self).form_valid(form)
        task = super(TaskUpdate, self).get_object()
        childs = form.cleaned_data.get('child_task').split('\r\n')
        for child in childs:
            ChildTask.objects.create(name=child, task=task).save()
        return valid


class TaskDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Task
    template_name = 'project_task/task_delete.html'
    success_url = reverse_lazy('projectman:list_task')

    def test_func(self):
        return check_project(self.request.user)


class TaskDetail(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Task
    template_name = 'project_task/task_detail.html'

    def test_func(self):
        dev = check_dev(self.request.user)
        prod = check_project(self.request.user)
        return prod or dev


@login_required
def task_moveup(request, pk):
    task = get_object_or_404(Task, pk=pk)
    lista = Task.objects.all()
    x = [e for e in lista if e.position == (task.position + 1)]
    if len(x) > 0:
        task.position = x[0].position
        x[0].position = x[0].position - 1
        task.save()
        x[0].save()
    print(Task.objects.all())
    return redirect('/list/task/')


@login_required
def task_movedown(request, pk):
    task = get_object_or_404(Task, pk=pk)
    lista = Task.objects.all()
    x = [e for e in lista if e.position == (task.position - 1)]
    if len(x) > 0:
        task.position = x[0].position
        x[0].position = x[0].position + 1
        task.save()
        x[0].save()
    print(x)
    print(x)
    return redirect('/list/task/')


@login_required
def get_task_child(request, task_pk):
    task = Task.objects.get(id=task_pk)
    child = serializers.serialize('json', task.task_child.all())
    data = json.loads(child)
    return render(request, 'project_task/child_task_list.html', {'data': data, 'task': task})


class CTaskDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = ChildTask
    template_name = 'inclusion_tags/modal_eliminar.html'
    success_url = reverse_lazy('projectman:list_task')

    def test_func(self):
        dev = check_dev(self.request.user)
        man = check_project(self.request.user)
        return dev or man


class CTaskCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = ChildTask
    template_name = 'project_task/child_task_create.html'
    form_class = CTaskRegisterForm
    success_url = reverse_lazy('projectman:list_task')

    def test_func(self):
        dev = check_dev(self.request.user)
        man = check_project(self.request.user)
        return dev or man


class CTaskUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = ChildTask
    template_name = 'project_task/child_task_create.html'
    form_class = CTaskRegisterForm
    success_url = reverse_lazy('projectman:list_task')

    def test_func(self):
        dev = check_dev(self.request.user)
        man = check_project(self.request.user)
        return dev or man
