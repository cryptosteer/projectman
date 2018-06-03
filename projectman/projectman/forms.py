from django import forms
from .models import User, Project, Task, Comment


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
        fields = [
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

        # = forms.CharField(widget=forms.Textarea(attrs={'rows':3, 'cols':3,}))

        widgets = {
<<<<<<< HEAD
=======
<<<<<<< HEAD
>>>>>>> df0bafbc90c916e43d9b9682827cd50aecc5be0c
            'title': forms.TextInput(attrs={'class':'from-control', 'style':'width:70%',}),
            'project_manager': forms.Select(attrs={'class':'from-control', 'style':'width:50%',}),
            'description': forms.Textarea(attrs={'class':'from-control', 'rows':4, 'style':'width:90%',}),
            'client' : forms.SelectMultiple(attrs={'class':'from-control', 'rows':4, 'style':'width:50%',}),
            'methodology': forms.TextInput(attrs={'class':'from-control', 'style':'width:40%',}),
            'budget': forms.NumberInput(attrs={'class':'from-control', 'style':'width:35%',}),
            'resources': forms.Textarea(attrs={'class':'from-control', 'rows':4, 'style':'width:90%',}),
            'time_start_real': forms.DateInput(attrs={'class':'from-control', 'type':'date', 'style':'width:35%',}),
            'time_end_real': forms.DateInput(attrs={'class':'from-control', 'type':'date', 'style':'width:35%',}),
            'time_start_estimated': forms.DateInput(attrs={'class':'from-control', 'type':'date', 'style':'width:35%',}),
            'time_end_estimated': forms.DateInput(attrs={'class':'from-control', 'type':'date', 'style':'width:35%',}),
<<<<<<< HEAD
=======
=======
            'title': forms.TextInput(attrs={'class':'from-control'}),
            'project_manager': forms.Select(attrs={'class':'from-control'}),
            'description': forms.Textarea(attrs={'class':'from-control', 'rows':4}),
            'client' : forms.SelectMultiple(),
            'methodology': forms.TextInput(attrs={'class':'from-control'}),
            'budget': forms.NumberInput(attrs={'class':'from-control'}),
            'resources': forms.Textarea(attrs={'class':'from-control', 'rows':4}),
            'time_start_real': forms.DateInput(attrs={'class':'from-control', 'type':'date'}),
            'time_end_real': forms.DateInput(attrs={'class':'from-control', 'type':'date'}),
            'time_start_estimated': forms.DateInput(attrs={'class':'from-control', 'type':'date'}),
            'time_end_estimated': forms.DateInput(attrs={'class':'from-control', 'type':'date'}),
>>>>>>> fa5dcf650e295d16a78090922298bee07923e71a
>>>>>>> df0bafbc90c916e43d9b9682827cd50aecc5be0c
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


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
<<<<<<< HEAD
        fields = [
=======
<<<<<<< HEAD
        fields = [
=======
        fields = '__all__'

        """  fields = [
>>>>>>> fa5dcf650e295d16a78090922298bee07923e71a
>>>>>>> df0bafbc90c916e43d9b9682827cd50aecc5be0c
            'name',
            'project',
            'description',
            'requeriments',
            'costs',
            'estimated_target_date',
            'responsable',
            'priority',
            'state',
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
            'name': forms.TextInput(attrs={'class':'from-control', 'style':'width:70%',}),
            'project': forms.Select(attrs={'class':'from-control', 'style':'width:70%',}),
            'description': forms.Textarea(attrs={'class':'from-control', 'rows':4, 'style':'width:90%',}),
            'requeriments' : forms.Textarea(attrs={'class':'from-control', 'rows':4, 'style':'width:90%',}),
            'costs': forms.NumberInput(attrs={'class':'from-control', 'style':'width:35%',}),
            'estimated_target_date': forms.DateInput(attrs={'class':'from-control', 'type':'date', 'style':'width:35%',}),
            'responsable': forms.Select(attrs={'class':'from-control', 'style':'width:50%',}),
            'priority': forms.Select(attrs={'class':'from-control', 'style':'width:20%',}),
            'state': forms.Select(attrs={'class':'from-control', 'style':'width:20%',}),
        }
<<<<<<< HEAD
=======
<<<<<<< HEAD
>>>>>>> df0bafbc90c916e43d9b9682827cd50aecc5be0c
    
    def clean(self):
        target_day = self.cleaned_data.get('estimated_target_date')
        project = self.cleaned_data.get('project')
        if target_day is not None and project.time_start_estimated is not None:
            if target_day < project.time_start_estimated:
                raise forms.ValidationError("Task's target day is incorrect")
        return self.cleaned_data


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
            'comment': forms.Textarea(attrs={'class': 'from-control', 'rows': 4, 'style': 'width:90%', }),
            'keyword': forms.TextInput(attrs={'class':'from-control', 'style':'width:70%',}),
        }

<<<<<<< HEAD
=======
=======
       """
>>>>>>> fa5dcf650e295d16a78090922298bee07923e71a
>>>>>>> df0bafbc90c916e43d9b9682827cd50aecc5be0c
