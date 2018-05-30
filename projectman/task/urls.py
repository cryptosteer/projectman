from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from task.views import MakeProject, MakeTask

urlpatterns = [
    url(r'^project/$', MakeProject.as_view(), name='build_project'),
    url(r'^task/$', MakeTask.as_view(), name='build_task'),
]
