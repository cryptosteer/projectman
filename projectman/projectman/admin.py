from django.contrib import admin
from django.forms import ModelForm
from .models import User, ProjectmanagerProfile, DeveloperProfile, ClientProfile, Project, Task


class UserCreationForm(ModelForm):

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


class UserAdmin(admin.ModelAdmin):
    form = UserCreationForm
    fieldsets = [
        ('User information', {'fields': ['username','password', 'name', 'is_project_manager', 'is_developer', 'is_client']}),
    ]


class ProjectmanagerProfileAdmin(admin.ModelAdmin):

    def has_add_permission(self, request):
        return False

class DeveloperProfileAdmin(admin.ModelAdmin):

    def has_add_permission(self, request):
        return False


class ClientProfileAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

class TaskInline(admin.StackedInline):
    model = Task
    extra = 1


class ProjectAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Project Basic Information', {'fields': ['name', 'description', 'project_man']}),
        ('Project Time Information', {'fields': ['finish_date']})
    ]
    inlines = [TaskInline]
    list_display = ('name', 'init_date', 'project_man', 'finish_date', 'num_task', 'task_done', 'task_process')



admin.site.register(User, UserAdmin)
admin.site.register(ProjectmanagerProfile, ProjectmanagerProfileAdmin)
admin.site.register(DeveloperProfile, DeveloperProfileAdmin)
admin.site.register(ClientProfile, ClientProfileAdmin)
admin.site.register(Project, ProjectAdmin)