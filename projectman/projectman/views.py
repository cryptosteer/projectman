from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import auth, messages
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.views.generic import FormView
from .forms import ProjectForm, TaskForm, UserCreationForm


# Checkers
def check_project(user):
    if user.is_active:
        return user.is_project_manager
    else:
        return False


def check_client(user):
    if user.is_active:
        return user.is_client
    else:
        return False


def check_dev(user):
    if user.is_active:
        return user.is_developer
    else:
        return False


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


# Create your views here.
class MakeProject(LoginRequiredMixin, UserPassesTestMixin, FormView):
    form_class = ProjectForm
    template_name = "task/project.html"

    def test_func(self):
        return check_project(self.request.user)


# Create your views here.
class MakeTask(LoginRequiredMixin, UserPassesTestMixin, FormView):
    form_class = TaskForm
    template_name = "task/task.html"
    login_url = '/login/'

    def test_func(self):
        dev = check_dev(self.request.user)
        prod = check_project(self.request.user)
        return prod or dev

"""
class ProjectList(ListView):
    model         = Project
    template_name = 'intelproject/project_list.html'
"""