from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib import auth, messages


from .forms import ProjectForm,TaskForm,CommentForm
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



@login_required
def register_project(request):
    if request.method == "POST":
        form = ProjectForm(data = request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
         form = ProjectForm()

    return render(request,'projectman/register_project.html', {'form':form})


@login_required
def task_from_project(request):
    if request.method == "POST":
        form = TaskForm(data = request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
         form = TaskForm()

    return render(request,'projectman/task_project.html', {'form':form})



@login_required
def comment_from_task(request):
    if request.method == "POST":
        form = CommentForm(data = request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
         form = CommentForm()
    return render(request,'projectman/comment_task.html', {'form':form})





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