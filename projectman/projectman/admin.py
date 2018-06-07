from django.contrib import admin
from django.db.models import Sum
from django.forms import Textarea
from django.db import models
from .models import User, ProjectmanagerProfile, DeveloperProfile, ClientProfile, Task, Project, Comment, Report, \
    Log  # , DetailBudget
from .forms import UserCreationForms, ProjectCreationForm, TaskCreationForm


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    form = UserCreationForms
    list_display = ('id', 'username', 'first_name', 'last_name', 'email', 'is_project_manager', 
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
                       'is_client',]
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
    list_display = ('id', 'user')
    def has_add_permission(self, request):
        return False


class TaskInLine(admin.StackedInline):
    model = Task
    formfield_overrides = {
       models.TextField: {'widget': Textarea(attrs={'style':'width:30%', 'rows':3})},
    }
    extra = 1


class CommentInLine(admin.StackedInline):
    model = Comment
    formfield_overrides = {
       models.TextField: {'widget': Textarea(attrs={'style':'width:30%', 'rows':3})},
    }
    extra = 1


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    form = ProjectCreationForm
    list_display = ('id','title', 'project_manager', 'description', 'methodology', 'resources', 'state',
                       'budget', 'price_hour_developer', 'hours_estimated', 'time_start_real', 'time_end_real')  #agregado price_hour_dev, hours_est
    formfield_overrides = {
       models.TextField: {'widget': Textarea(attrs={'style':'width:30%', 'rows':3})},
    }
    fieldsets = [
        (None, {'fields':['title']}),
        ('Project information', {'fields':['project_manager', 'description', 'methodology','resources','state', 'budget', 'hours_estimated', 'price_hour_developer']}),  #agregado price_hour_dev, hours_est
        ('Clients', {'fields': ['client',],'classes':['collapse']}),
        ('Estimate time duration',{'fields':[ 'time_start_estimated', 'time_end_estimated'],}),
        ('Real time duration', {'fields': ['time_start_real', 'time_end_real'], }),
    ]
    inlines = [TaskInLine]


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    form = TaskCreationForm
    list_display = ('name', 'project', 'description', 'requeriments', 'costs',
                    'estimated_target_date', 'responsable', 'priority', 'state')
    formfield_overrides = {
       models.TextField: {'widget': Textarea(attrs={'style':'width:30%', 'rows':3})},
    }
    inlines = [CommentInLine]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('task', 'owner', 'comment', 'keyword', 'date_created')



@admin.register(Report)                #agregado
class AdminReport(admin.ModelAdmin):

    list_display = ('id', 'project')
    pass

   #list_display = ('id', 'project', 'Presupuesto', 'Valor_HT_desarrollador', 'HT_estimadas')

    #list_filter = ('course', 'student')
#admin.site.register(DetailBudget)
#admin.site.register(Informe)
admin.site.register(Log)