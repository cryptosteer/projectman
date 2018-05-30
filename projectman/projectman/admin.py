from django.contrib import admin
from .models import User, ProjectmanagerProfile, DeveloperProfile, ClientProfile, Task, Project, Comment
from .forms import UserCreationForm, ProjectCreationForm, TaskCreationForm


class UserAdmin(admin.ModelAdmin):
    form = UserCreationForm
    fieldsets = [
        ('User information', {
            'fields': ['username',
                       'password',
                       'name',
                       'is_project_manager',
                       'is_developer',
                       'is_client',]
        }),
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


class TaskInLine(admin.StackedInline):
    model = Task
    extra = 1


class CommentInLine(admin.TabularInline):
    model = Comment
    extra = 1


class ProjectAdmin(admin.ModelAdmin):
    form = ProjectCreationForm
    fieldsets = [
        (None, {'fields':['title']}),
        ('Project information', {'fields':['description', 'project_manager', 'budget']}),
        ('Clients', {'fields': ['client',],'classes':['collapse']}),
        ('Estimate time duration',{'fields':[ 'time_start_estimated', 'time_end_estimated'],}),
        ('Real time duration', {'fields': ['time_start_real', 'time_end_real'], }),
    ]
    inlines = [TaskInLine]


class TaskAdmin(admin.ModelAdmin):
    form = TaskCreationForm
    inlines = [CommentInLine]


admin.site.register(User, UserAdmin)
admin.site.register(ProjectmanagerProfile, ProjectmanagerProfileAdmin)
admin.site.register(DeveloperProfile, DeveloperProfileAdmin)
admin.site.register(ClientProfile, ClientProfileAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(Comment)
