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
    url(r'^hola/$', TemplateView.as_view(template_name='index.html'), name='new'),
    url(r'^register/$', views.register_project, name='Register_Project'),
    url(r'^task/$', views.task_from_project, name='Register_Task'),

    url(r'^comments/$', views.comment_from_task, name='Task_Comments'),

]