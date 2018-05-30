from django.contrib import admin
from django.forms import ModelForm
from .models import User,ProjectmanagerProfile,DeveloperProfile,ClientProfile, Project,Task,Comments,Members
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


@admin.register(Project)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name','description','start_date')


@admin.register(Task)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name','state','description','start_date')




@admin.register(Members)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('user_id','task_id','name')



admin.site.register(User, UserAdmin)
admin.site.register(ProjectmanagerProfile, ProjectmanagerProfileAdmin)
admin.site.register(DeveloperProfile, DeveloperProfileAdmin)
admin.site.register(ClientProfile, ClientProfileAdmin)


admin.site.register(Comments)

