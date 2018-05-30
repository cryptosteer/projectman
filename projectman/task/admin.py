from django.contrib import admin
from task.models import Project, Task


# Register your models here.

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


admin.site.register(Project, ProjectAdmin)
