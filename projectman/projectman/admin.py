from django.contrib import admin
from .models import User, ProjectmanagerProfile, DeveloperProfile, ClientProfile, Task, Project
from .forms import UserCreationForm


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


class TaskInLine(admin.TabularInline):
    model = Task
    extra = 1


class ProjectAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields':['tittle']}),
        ('Project information', {'fields':['description',]}),
        ('Date information',{'fields':[ 'start_day', 'end_day'],})
    ]
    inlines = [TaskInLine]

admin.site.register(User, UserAdmin)
admin.site.register(ProjectmanagerProfile, ProjectmanagerProfileAdmin)
admin.site.register(DeveloperProfile, DeveloperProfileAdmin)
admin.site.register(ClientProfile, ClientProfileAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Task)