from django.conf.urls import url
from projectman import views

app_name = 'projectman'
urlpatterns = [
    #vista index
    url(r'^$', views.index, name='index'),
    url(r'^$modal/', views.modalComment, name='modal_comment'),

    #vistas login, logout y dashboard
    url(r'^login/$', views.login_user, name='login'),
    url(r'^register/$', views.RegisterUser.as_view(), name='register_user'),
    url(r'^dashboard/$', views.dashboard, name='dashboard'),
    url(r'^logout/$', views.logout, name='logout'),

    #vistas Crear, Listar, Actualizar y Eliminar del model Project
    url(r'^list/project/$', views.ProjectList.as_view(), name='list_project'),
    url(r'^detail/project/(?P<pk>[0-9]+)/$', views.ProjectDetail.as_view(), name='detail_project'),
    url(r'^create/project/$', views.ProjectCreate.as_view(), name='build_project'),
    url(r'^update/project/(?P<pk>[0-9]+)/$', views.ProjectUpdate.as_view(), name='update_project'),
    url(r'^delete/project/(?P<pk>[0-9]+)/$', views.ProjectDelete.as_view(), name='delete_project'),
    url(r'^list/project/client/(?P<pk>[0-9]+)/$', views.project_list_filter, name='list_project_client'),

    #vistas Crear, Listar, Actualizar y Eliminar del model Task
    url(r'^list/task/$', views.TaskList.as_view(), name='list_task'),
    url(r'^list/task/(?P<pk>[0-9]+)/$', views.task_list_filter, name='list_task_filter'),
    url(r'^detail/task/(?P<pk>[0-9]+)/$', views.TaskDetail.as_view(), name='detail_task'),
    url(r'^create/task/$', views.TaskCreate.as_view(), name='build_task'),
    url(r'^update/task/(?P<pk>[0-9]+)/$', views.TaskUpdate.as_view(), name='update_task'),
    url(r'^delete/task/(?P<pk>[0-9]+)/$', views.TaskDelete.as_view(), name='delete_task'),

    #vistas Crear, Listar, Actualizar y Eliminar del model Comment
    url(r'^list/comment/(?P<pk>[0-9]+)/$', views.comment_list_filter, name='list_comment_filter'),
    url(r'^list/comment/$', views.CommentList.as_view(), name='list_comment'),
    url(r'^detail/commet/(?P<pk>[0-9]+)/$', views.CommentDetail.as_view(), name='detail_comment'),
    url(r'^create/comment/$', views.CommentCreate.as_view(), name='build_comment'),
    url(r'^update/comment/(?P<pk>[0-9]+)/$', views.CommentUpdate.as_view(), name='update_comment'),
    url(r'^delete/comment/(?P<pk>[0-9]+)/$', views.CommentDelete.as_view(), name='delete_comment'),

    #informes costos de proyectos
    url(r'^report/(?P<pk>[0-9]+)/$', views.report_cost, name='report_cost'),

]
