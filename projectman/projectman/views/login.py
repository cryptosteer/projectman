from django.contrib import auth, messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.generic import CreateView

from ..forms import RegisterUserForm
from ..models import User


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
        return render(request, 'projectman/index.html')


def login_user(request):
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
                    messages.error(request, "Error en usuario y/o contraseña")
                    return redirect('projectman:login')
        else:
            return render(request, 'projectman/login.html')


class RegisterUser(CreateView):
    model = User
    template_name = 'projectman/registrer_user.html'
    form_class = RegisterUserForm

    def form_valid(self, form):
        form.save()
        usuario = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        usuario = authenticate(username=usuario, password=password)
        login(self.request, usuario)
        return redirect('projectman:login')


@login_required
def dashboard(request):
    return render(request, "projectman/dashboard.html")


@login_required
def logout(request):
    auth.logout(request)
    return redirect('projectman:index')
