from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.views.generic import FormView
from task.forms import ProjectForm, TaskForm


# Checkers
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


# Create your views here.
class MakeProject(LoginRequiredMixin, UserPassesTestMixin, FormView):
    form_class = ProjectForm
    template_name = "task/project.html"

    def test_func(self):
        return check_project(self.request.user)


# Create your views here.
class MakeTask(LoginRequiredMixin, UserPassesTestMixin, FormView):
    form_class = TaskForm
    template_name = "task/task.html"
    login_url = '/login/'

    def test_func(self):
        dev = check_dev(self.request.user)
        prod = check_project(self.request.user)
        return dev or prod

