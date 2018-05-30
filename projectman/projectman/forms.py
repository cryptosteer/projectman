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
        fields = ('time_start_real', 'time_end_real')

    def clean(self):
        start_day = self.cleaned_data.get('time_start_real')
        end_day = self.cleaned_data.get('time_end_real')
        if start_day > end_day:
            raise forms.ValidationError("Dates are incorrect")
        return self.cleaned_data


class TaskCreationForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = ('estimated_target_date', 'priority', 'state', 'project')




    def clean(self):
        target_day = self.cleaned_data.get('estimated_target_date')
        project = self.cleaned_data.get('project')
        if target_day > project.time_end_real or target_day < project.time_start_real:
            raise forms.ValidationError("Task's target day is incorrect")
        return self.cleaned_data
