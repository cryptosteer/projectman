from django import forms
from projectman.models import Project, Task

class ProjectForm(forms.ModelForm):

    class Meta:
        model = Project
        fields = "__all__"


class TaskForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = "__all__"