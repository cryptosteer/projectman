from django import forms
from .models import User, Project, Task


class UserCreationForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('email','name')

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
        fields = ('time_start_real', 'time_end_real', 'time_start_estimated', 'time_end_estimated')

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
        fields = ('name', 'description', 'requeriments', 'project', 'costs', 'estimated_target_date', 'priority', 'state', 'responsable', )

    def clean(self):
        target_day = self.cleaned_data.get('estimated_target_date')
        project = self.cleaned_data.get('project')
        if target_day is not None and project.time_start_estimated is not None:
            if target_day < project.time_start_estimated:
                raise forms.ValidationError("Task's target day is incorrect")
        return self.cleaned_data


#class ProyectoForm(forms.ModelForm):

 #   def __init__(self, *args, **kwargs):
  #      super().__init__(*args, **kwargs)
   #     self.fields['estado'].empty_label = "- Seleccione -"
    #    self.fields['estado'].initial = 1


    #class Meta:
     #   model = Proyecto
      #  fields = ('nombre', 'descripcion', 'estado', 'usuarios_expertos', )

       # labels = {
        #    'nombre': 'Nombre',
         #   'descripcion': 'Descripción',
          #  'estado': 'Estado',
           # 'usuarios_expertos': 'Usuarios'
#        }

 #       widgets = {
  #          'nombre': forms.TextInput(attrs={
   #             'class': 'form-control',
    #            'placeholder': placeholderText
     #       }),
      #      'descripcion': forms.Textarea(attrs={
       #         'class': 'form-control',
        #        'placeholder': placeholderText,
          #      'rows': '3'
         #   }),
           # 'estado': forms.Select(attrs={
            #    'class': 'form-control selectpicker',
             #   'data-live-search': 'true',
              #  'id': 'estado',
#            }),
 #           'usuarios_expertos': forms.SelectMultiple(attrs={
  #              'class': 'form-control selectpicker',
   #             'data-live-search': 'true',
    #            'data-size': '15',
     #           'title': 'Agregar...',
      #          'data-selected-text-format': 'count',
       #         'data-actions-box': 'true',
        #        'id': 'usuario',
         #   }),
#        }
