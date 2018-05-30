from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib import auth, messages


# Create your views here.
def index(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        return render(request, 'projectman/index.html')


def login(request):
    if request.user.is_authenticated and request.user.is_active:
        return redirect('dashboard')
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
                    return redirect('dashboard')
                else:
                    return redirect('login')
        else:
            return render(request, 'projectman/login.html')


def dashboard(request):
    return render(request, "projectman/dashboard.html")


def help(request):
    return render(request, 'projectman/help.html')


@login_required
def logout(request):
    auth.logout(request)
    return redirect('login')