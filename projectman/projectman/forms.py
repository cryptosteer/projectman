from django import forms
from .models import User, Project, Task


class UserCreationForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('__all__')

    def save(self,commit=True):
        user=super(UserCreationForm,self).save(commit=False)
        if len(User.objects.filter(username=user.username))==0:
            user.set_password(self.cleaned_data["password"])
        else:
            if user.password != User.objects.get(username=user.username).password:
                user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class ProjectCreationForm(forms.ModelForm):

    class Meta:
        model = Project
        fields = ('__all__')

    def clean(self):
        start_day_real = self.cleaned_data.get('time_start_real')
        end_day_real = self.cleaned_data.get('time_end_real')
        start_day_estimated = self.cleaned_data.get('time_start_estimated')
        end_day_estimated = self.cleaned_data.get('time_end_estimated')
        if start_day_real is not None and end_day_real is not None:
            if start_day_real > end_day_real:
                raise forms.ValidationError("Real times/dates are incorrect")
        if start_day_estimated is not None and end_day_estimated is not None:
            if start_day_estimated > end_day_estimated:
                raise forms.ValidationError("Estimated times/dates are incorrect")
        return self.cleaned_data


class TaskCreationForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = ('__all__')

    def clean(self):
        target_day = self.cleaned_data.get('estimated_target_date')
        project = self.cleaned_data.get('project')
        if target_day is not None and project.time_start_estimated is not None:
            if target_day < project.time_start_estimated:
                raise forms.ValidationError("Task's target day is incorrect")
        return self.cleaned_data



class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = '__all__'
        """[
            'title',
            'project_manager',
            'description',
            'client',
            'methodology',
            'budget',
            'resources',
            'time_start_real',
            'time_end_real',
            'time_start_estimated',
            'time_end_estimated',
        ]

        labels = {
            'title': 'Nombre de Proyecto',
            'project_manager': 'Project Manager',
            'description': 'Descripción',
            'client': 'Cliente',
            'methodology': 'Metodología',
            'budget' : 'Presupuesto',
            'resources' : 'Recursos',
            'time_start_real': 'Fecha inicio real',
            'time_end_real': 'Fecha final real',
            'time_start_estimated': 'Fecha inicio estimado',
            'time_end_estimated': 'Fecha final estimado',
        }

        widgets = {
            'title': forms.TextInput(),
            'project_manager': forms.TextInput(),
            'description': forms.NumberInput(),
            'client' : forms.TextInput(),
            'methodology': forms.DateInput(),
        }
"""

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = '__all__'
        """
        fields = [
            'name',
            'project',
            'description',
            'requeriments',
            'costs',
            'estimated_time',
        ]

        labels = {
            'name': 'Nombre Tarea',
            'project': 'Nombre Proyecto',
            'description': 'Descripcion',
            'requeriments': 'Requerimientos',
            'costs': 'Costos',
            'estimated_time': 'Tiempo estimado',
        }

        widgets = {
            'name': forms.TextInput(),
            'project': forms.Select(),
            'description': forms.TextInput(),
            'requeriments' : forms.TextInput(),
            'costs': forms.NumberInput(),
            'estimated_time': forms.DateInput(),
        }
       """