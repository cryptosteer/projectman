from django.forms import ModelForm
from .models import Project,Task,Comments,User


class UserCreationForm(ModelForm):

    class Meta:
        model = User
        fields = ('email','name')

    def save(self,commit=True):
        user=super(UserCreationForm,self).save(commit=False)
        if len(User.objects.filter(username=user.username)) == 0:
            user.set_password(self.cleaned_data["password"])
        else:
            if user.password != User.objects.get(username=user.username).password:
                user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user



class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = '__all__'


class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = '__all__'


class CommentForm(ModelForm):
    class Meta:
        model = Comments
        fields = '__all__'