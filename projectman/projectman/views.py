from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib import auth, messages

# Create your views here.

@login_required
def index(request):
    user=auth.get_user(request)
    print(user.is_project_manager)
    return render(request, 'projectman/index.html')


def login(request):
    if str(auth.get_user(request)) != 'AnonymousUser':
        return HttpResponseRedirect('../')
    username=request.POST.get('username')
    password=request.POST.get('password')
    user=auth.authenticate(username=username, password=password)
    if user is not None and user.is_active:
        auth.login(request,user)
        return HttpResponseRedirect('../')
    else:
        if request.POST.get('username') is not None:
            messages.error(request,"Error en usuario y/o contraseña")
        return render(request, 'projectman/login.html')

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



def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('../help/')

def help(request):
    return render(request, 'projectman/help.html')


@login_required
@user_passes_test(check_dev)
def private():
    return "Hello"


from .forms import Formulito

def prueba_form(request):
    return render(request, 'index.html', {'form': Formulito})