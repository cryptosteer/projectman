from django.contrib import admin
from django.forms import Textarea
from django.db import models
from .models import User, ProjectmanagerProfile, DeveloperProfile, ClientProfile, Task, Project, Comment
from .forms import UserCreationForm, ProjectCreationForm, TaskCreationForm


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    form = UserCreationForm
    list_display = ('username', 'first_name', 'last_name', 'email', 'is_project_manager',
                    'is_developer', 'is_client')
    list_filter = ('is_project_manager', 'is_developer', 'is_client')
    fieldsets = [
        ('User information', {
            'fields': ['username',
                       'password',
                       'first_name',
                       'last_name',
                       'email',
                       'is_project_manager',
                       'is_developer',
                       'is_client']
        }),
    ]


@admin.register(ProjectmanagerProfile)
class ProjectmanagerProfileAdmin(admin.ModelAdmin):

    def has_add_permission(self, request):
        return False


@admin.register(DeveloperProfile)
class DeveloperProfileAdmin(admin.ModelAdmin):

    def has_add_permission(self, request):
        return False


@admin.register(ClientProfile)
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


class TaskInLine(admin.StackedInline):
    model = Task
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'style': 'width:30%', 'rows': 3})},
    }
    extra = 1


class CommentInLine(admin.StackedInline):
    model = Comment
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'style': 'width:30%', 'rows': 3})},
    }
    extra = 1


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    form = ProjectCreationForm
    list_display = ('title', 'project_manager', 'description', 'methodology', 'resources',
                    'budget', 'time_start_real', 'time_end_real')
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'style': 'width:30%', 'rows': 3})},
    }
    fieldsets = [
        (None, {'fields': ['title']}),
        ('Project information', {'fields': ['project_manager', 'description', 'methodology', 'resources', 'budget']}),
        ('Clients', {'fields': ['client', ], 'classes': ['collapse']}),
        ('Estimate time duration', {'fields': ['time_start_estimated', 'time_end_estimated'], }),
        ('Real time duration', {'fields': ['time_start_real', 'time_end_real'], }),
    ]
    inlines = [TaskInLine]


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    form = TaskCreationForm
    list_display = ('name', 'project', 'description', 'requeriments', 'costs',
                    'estimated_target_date', 'responsable', 'priority', 'state')
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'style': 'width:30%', 'rows': 3})},
    }
    inlines = [CommentInLine]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('task', 'owner', 'comment', 'keyword', 'date_created')
