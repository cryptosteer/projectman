from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib import auth, messages

# Create your views here.


def index(request):
    if str(auth.get_user(request)) == 'AnonymousUser':
        return HttpResponseRedirect('help/')
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

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('../help/')

def help(request):
    return render(request, 'projectman/help.html')