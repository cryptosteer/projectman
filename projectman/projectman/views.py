from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import auth, messages
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin, PermissionRequiredMixin

from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.core.urlresolvers import reverse_lazy
from .forms import ProjectForm, TaskForm, UserCreationForm, CommentForm
from .models import Project, Task, Comment


# Views
def index(request):
    if request.user.is_authenticated.value:
        return redirect('projectman:dashboard')
    else:
        return render(request, 'projectman/index2.html')


def login(request):
    if request.user.is_authenticated and request.user.is_active:
        return redirect('projectman:dashboard')
    else:
        if request.method == 'POST':

            if request.POST.get('username') is None:
                messages.error(request, "Error en usuario y/o contraseña")
            else:
                username = request.POST.get('username')
                password = request.POST.get('password')
                user = auth.authenticate(username=username, password=password)
                if user is not None and user.is_active:
                    auth.login(request, user)
                    return redirect('projectman:dashboard')
                else:
                    return redirect('projectman:login')
        else:
            return render(request, 'projectman/login2.html')


@login_required
def dashboard(request):
    return render(request, "projectman/dashboard.html")


def help(request):
    return render(request, 'projectman/help.html')


@login_required
def logout(request):
    auth.logout(request)
    return redirect('projectman:index')


# Vistas del modelo Project
class ProjectCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Project
    form_class = ProjectForm
    template_name = "project_task/project_create.html"
    permission_required = 'projectman.add_project'
    success_url = reverse_lazy('projectman:list_project')


class ProjectList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Project
    template_name = 'project_task/project_list.html'
    permission_required = 'projectman.view_project'

    def test_func(self):
        return self.request.user.is_project_manager


class ProjectUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'project_task/project_create.html'
    permission_required = 'projectman.change_project'
    success_url = reverse_lazy('projectman:list_project')


class ProjectDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Project
    template_name = 'project_task/project_delete.html'
    permission_required = 'projectman.delete_project'
    success_url = reverse_lazy('projectman:list_project')


class ProjectDetail(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Project
    template_name = 'project_task/project_detail.html'
    permission_required = 'projectman.view_project'


# Vistas del modelo Task.
class TaskCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = "project_task/task_create.html"
    permission_required = 'projectman.add_task'
    success_url = reverse_lazy('projectman:list_task')


@login_required
def task_list_filter(request, pk):
    tareas = Task.objects.filter(project=pk)
    context = {'tareas': tareas}
    return render(request, 'project_task/task_list_filter.html', context)


class TaskList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Task
    template_name = 'project_task/task_list.html'
    permission_required = 'projectman.view_task'
    success_url = reverse_lazy('projectman:list_comment')


class TaskUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'project_task/task_create.html'
    permission_required = 'projectman.change_task'


class TaskDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Task
    template_name = 'project_task/task_delete.html'
    permission_required = 'projectman.delete_task'
    success_url = reverse_lazy('projectman:list_project')


class TaskDetail(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Task
    template_name = 'project_task/task_detail.html'
    permission_required = 'projectman.view_task'


# Vistas modelo Comment
@login_required
def comment_list_filter(request, pk):
    comment = Comment.objects.filter(task=pk)
    context = {'comment': comment}
    return render(request, 'project_task/comment_list_filter.html', context)


class CommentCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = "project_task/comment_create.html"
    success_url = reverse_lazy('projectman:task_lista')

    def test_func(self):
        return self.request.user.is_project_manager

"""
@login_required
def task_list_filter(request, pk):
    tareas = Task.objects.filter(project=pk)
    context = {'tareas':tareas}
    return render(request, 'projectman/task_list2.html', context)
"""


class CommentList(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Comment
    template_name = 'project_task/comment_list.html'

    def test_func(self):
        return self.request.user.is_project_manager


class CommentUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'project_task/comment_create.html'
    success_url = reverse_lazy('projectman:list_comment')

    def test_func(self):
        return self.request.user.is_project_manager


class CommentDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'inclusion_tags/modal_eliminar.html'
    success_url = reverse_lazy('projectman:task_lista')

    def test_func(self):
        return self.request.user.is_project_manager


class CommentDetail(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Comment
    template_name = 'project_task/comment_detail.html'

    def test_func(self):
        return self.request.user.is_project_manager


@login_required
def modalComment(request):
    return render(request, 'project_task/prueba_modal.html', {})
