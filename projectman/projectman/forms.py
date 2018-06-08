from django import forms
from django.core.exceptions import ObjectDoesNotExist
from .models import User, Project, Task, Comment, ChildTask


class UserCreationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        if len(User.objects.filter(username=user.username)) == 0:
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
        fields = '__all__'

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

    def save(self, commit=True):
        project = super(ProjectCreationForm, self).save(commit=False)
        if len(Project.objects.all()) > 0:
            project.position = Project.objects.all()[len(Project.objects.all()) - 1].position + 1
        else:
            project.position += 1
        if commit:
            project.save()
        return project


class TaskCreationForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'project', 'description', 'requeriments', 'costs',
                    'estimated_target_date', 'responsable', 'priority', 'state',]

    def clean(self):
        target_day = self.cleaned_data.get('estimated_target_date')
        project = self.cleaned_data.get('project')
        if target_day is not None and project.time_start_estimated is not None:
            if target_day < project.time_start_estimated:
                raise forms.ValidationError("Task's target day is incorrect")
        return self.cleaned_data

    def save(self, commit=True):
        task = super(TaskCreationForm, self).save(commit=False)
        if len(Task.objects.all()) > 0:
            task.position = Task.objects.all()[len(Task.objects.all()) - 1].position + 1
        else:
            task.position += 1
        if commit:
            task.save()
        return task


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = [
            'title',
            'project_manager',
            'description',
            'client',
            'methodology',
            'budget',
            'resources',
            'time_start_estimated',
            'time_end_estimated',
        ]

        labels = {
            'title': 'Nombre de Proyecto',
            'project_manager': 'Project Manager',
            'description': 'Descripción',
            'client': 'Cliente',
            'methodology': 'Metodología',
            'budget': 'Presupuesto',
            'resources': 'Recursos',
            'time_start_real': 'Fecha inicio real',
            'time_end_real': 'Fecha final real',
            'time_start_estimated': 'Fecha inicio estimado',
            'time_end_estimated': 'Fecha final estimado',
        }

        # = forms.CharField(widget=forms.Textarea(attrs={'rows':3, 'cols':3,}))

        widgets = {

            'title': forms.TextInput(attrs={'class': 'from-control', 'style': 'width:70%', }),
            'project_manager': forms.Select(attrs={'class': 'from-control', 'style': 'width:50%', }),
            'description': forms.Textarea(attrs={'class': 'from-control', 'rows': 4, 'style': 'width:90%', }),
            'client': forms.SelectMultiple(attrs={'class': 'from-control', 'rows': 4, 'style': 'width:50%', }),
            'methodology': forms.TextInput(attrs={'class': 'from-control', 'style': 'width:40%', }),
            'budget': forms.NumberInput(attrs={'class': 'from-control', 'style': 'width:35%', }),
            'resources': forms.Textarea(attrs={'class': 'from-control', 'rows': 4, 'style': 'width:90%', }),
            'time_start_real': forms.DateInput(attrs={'class': 'from-control', 'type': 'date', 'style': 'width:35%', }),
            'time_end_real': forms.DateInput(attrs={'class': 'from-control', 'type': 'date', 'style': 'width:35%', }),
            'time_start_estimated': forms.DateInput(
                attrs={'class': 'from-control', 'type': 'date', 'style': 'width:35%', }),
            'time_end_estimated': forms.DateInput(
                attrs={'class': 'from-control', 'type': 'date', 'style': 'width:35%', }),

        }

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

    def save(self, commit=True):
        project = super(ProjectForm, self).save(commit=False)
        if len(Project.objects.all()) > 0:
            project.position = Project.objects.all()[len(Project.objects.all())-1].position+1
        else:
            project.position += 1
        if commit:
            project.save()
        return project


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = [

            'name',
            'project',
            'description',
            'requeriments',
            'costs',
            'estimated_target_date',
            'responsable',
            'priority',
            'state',
            'position'
        ]

        labels = {
            'name': 'Nombre Tarea',
            'project': 'Nombre Proyecto',
            'description': 'Descripcion',
            'requeriments': 'Requerimientos',
            'costs': 'Costos',
            'estimated_target_date': 'Tiempo estimado',
            'responsable': 'Responsable',
            'priority': 'Prioridad',
            'state': 'Estado',
        }

        widgets = {
            'name': forms.TextInput(attrs={'class': 'from-control', 'style': 'width:70%', }),
            'project': forms.Select(attrs={'class': 'from-control', 'style': 'width:70%', }),
            'description': forms.Textarea(attrs={'class': 'from-control', 'rows': 4, 'style': 'width:90%', }),
            'requeriments': forms.Textarea(attrs={'class': 'from-control', 'rows': 4, 'style': 'width:90%', }),
            'costs': forms.NumberInput(attrs={'class': 'from-control', 'style': 'width:35%', }),
            'estimated_target_date': forms.DateInput(
                attrs={'class': 'from-control', 'type': 'date', 'style': 'width:35%', }),
            'responsable': forms.Select(attrs={'class': 'from-control', 'style': 'width:50%', }),
            'priority': forms.Select(attrs={'class': 'from-control', 'style': 'width:20%', }),
            'state': forms.Select(attrs={'class': 'from-control', 'style': 'width:20%', }),
        }

    def clean_state(self):
        state = self.cleaned_data.get('state')
        name = self.cleaned_data.get('name')
        if state == 1:
            try:
                task = Task.objects.get(name=name)
            except ObjectDoesNotExist:
                raise forms.ValidationError('El estado no puede ser done (La tarea apenas se crea)', code='invalid')
            else:
                child = [c.complete for c in task.task_child.all()]
                if all(child):
                    return state
                else:
                    raise forms.ValidationError('El estado no puede ser done (Existen tareas hijas pendientes)',
                                                code='invalid')
        return state

    def clean(self):
        target_day = self.cleaned_data.get('estimated_target_date')
        project = self.cleaned_data.get('project')
        if target_day is not None and project.time_start_estimated is not None:
            if target_day < project.time_start_estimated:
                raise forms.ValidationError("Task's target day is incorrect")
        return self.cleaned_data

    def save(self, commit=True):
        task = super(TaskForm, self).save(commit=False)
        if len(Task.objects.all()) > 0:
            task.position = Task.objects.all()[len(Task.objects.all())-1].position+1
        else:
            task.position += 1
        if commit:
            task.save()
        return task


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [
            'task',
            'owner',
            'comment',
            'keyword',
        ]

        labels = {
            'task': 'Tarea',
            'owner': 'Autor',
            'comment': 'Comentario',
            'keyword': 'Palabra Clave',
        }

        widgets = {
            'task': forms.Select(attrs={'class': 'from-control', 'style': 'width:70%', }),
            'owner': forms.Select(attrs={'class': 'from-control', 'style': 'width:70%', }),
            'comment': forms.Textarea(attrs={'class': 'from-control', 'rows': 10, 'style': 'width:90%', }),
            'keyword': forms.TextInput(attrs={'class': 'from-control', 'style': 'width:70%', }),
        }


class RegisterUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
        )

        labels = {
            'username': 'Nombre de usuario',
            'first_name': 'Nombre',
            'last_name': 'Apellidos',
            'email': 'Email',
        }


class CTaskRegisterForm(forms.ModelForm):
    class Meta:
        model = ChildTask
        fields = '__all__'

    def clean_complete(self):
        complete = self.cleaned_data.get('complete')
        name = self.cleaned_data.get('name')
        if complete:
            try:
                ChildTask.objects.get(name=name)
            except ObjectDoesNotExist:
                raise forms.ValidationError("Complete no puede estar marcado (La mini tarea apenas se crea)",
                                            code='invalid')
            else:
                return complete
        return complete

    def save(self, commit=True):
        child = super(CTaskRegisterForm, self).save()
        task = child.task
        if task.state == 1 or task.state == 3:
            task.state = 2
            task.save()
        return child
