from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LoginView, LogoutView 

class SignOutView(LogoutView):
    pass
    
class SignInView(LoginView):
    template_name = 'perfiles/iniciar_sesion.html'

# Create your views here.
