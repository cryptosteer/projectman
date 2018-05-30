from django.conf.urls import url
from django.views.generic import TemplateView

from projectman import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.login, name='login'),
    url(r'^dashboard/$', views.dashboard, name='dashboard'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^help/$', views.help, name='help'),
    url(r'^create/project/$', views.MakeProject.as_view(), name='build_project'),
    url(r'^create/task/$', views.MakeTask.as_view(), name='build_task'),
]
