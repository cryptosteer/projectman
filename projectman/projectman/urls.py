from django.conf.urls import url

from projectman import views


app_name = 'projectman'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.login, name='login'),
    url(r'^dashboard/$', views.dashboard, name='dashboard'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^help/$', views.help, name='help'),
    url(r'^list/project/$', views.ProjectList.as_view(), name='list_project'),
    url(r'^create/project/$', views.ProjectCreate.as_view(), name='build_project'),
    url(r'^update/project/(?P<pk>[0-9]+)/$', views.ProjectUpdate.as_view(), name='update_project'),
    url(r'^delete/project/(?P<pk>[0-9]+)/$', views.ProjectDelete.as_view(), name='delete_project'),
    url(r'^create/task/$', views.TaskCreate.as_view(), name='build_task'),
]
