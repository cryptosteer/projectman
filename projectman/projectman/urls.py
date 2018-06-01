from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^help/$', views.help, name='help'),
    url(r'^new/$', views.private, name='new'),
    url(r'^prueba/$', views.prueba_form, name='prueba'),
    url(r'^hola/$', TemplateView.as_view(template_name='index.html'), name='new'),
]