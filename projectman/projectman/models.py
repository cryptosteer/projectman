from __future__ import unicode_literals
from django.contrib.auth.models import Group, AbstractUser
from django.db import models


class User(AbstractUser):
    is_project_manager=models.BooleanField(default=False)
    is_developer=models.BooleanField(default=False)
    is_client = models.BooleanField(default=False)
    name = models.CharField(max_length=64,default="")

    def get_projectmanager_profile(self):
        projectmanager_profile=None
        if hasattr(self,'projectmanagerprofile'):
            projectmanager_profile=self.projectmanagerprofile
        return projectmanager_profile

    def get_developer_profile(self):
        developer_profile=None
        if hasattr(self,'developerprofile'):
            developer_profile=self.developerprofile
        return developer_profile

    def get_client_profile(self):
        client_profile=None
        if hasattr(self,'clientprofile'):
            client_profile=self.clientprofile
        return client_profile

    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)
        if self.is_project_manager:
            if len(ProjectmanagerProfile.objects.filter(user=self)) == 0:
                ProjectmanagerProfile.objects.create(user=self)
        else:
            if len(ProjectmanagerProfile.objects.filter(user=self)) != 0:
                ProjectmanagerProfile.delete(ProjectmanagerProfile.objects.get(user=self))

        if self.is_developer:
            if len(DeveloperProfile.objects.filter(user=self)) == 0:
                DeveloperProfile.objects.create(user=self)
        else:
            if len(DeveloperProfile.objects.filter(user=self)) != 0:
                DeveloperProfile.delete(DeveloperProfile.objects.get(user=self))

        if self.is_client:
            if len(ClientProfile.objects.filter(user=self)) == 0:
                ClientProfile.objects.create(user=self)
        else:
            if len(ClientProfile.objects.filter(user=self)) != 0:
                ClientProfile.delete(ClientProfile.objects.get(user=self))

    class Meta:
        db_table = 'auth_user'


class ProjectmanagerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cellphone = models.CharField(max_length=10, default="")

    def __str__(self):
        return self.user.name


class DeveloperProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    github = models.CharField(max_length=60, default="")

    def __str__(self):
        return self.user.name


class ClientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cellphone = models.CharField(max_length=10, default="")

    def __str__(self):
        return self.user.name


# Create your models here.
class Project(models.Model):
    name = models.CharField(max_length=20, null=False, blank=False)
    description = models.TextField(null=False, blank=False)
    init_date = models.DateTimeField(auto_now_add=True, editable=False, blank=True)
    finish_date = models.DateField(null=True, blank=True)

    project_man = models.OneToOneField(ProjectmanagerProfile,
                                       on_delete=models.SET_NULL,
                                       null=True,
                                       blank=True,
                                       related_name='owner'
                                       )

    def num_task(self):
        return Task.objects.filter(project=self).count()

    def task_done(self):
        return Task.objects.filter(project=self, status='Done').count()

    def task_process(self):
        return Task.objects.filter(project=self, status='Process').count()

    def __str__(self):
        return self.name


class Task(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    description = models.TextField(null=False)
    init_date = models.DateTimeField(auto_now_add=True, editable=False, blank=True)
    finish_date = models.DateField(null=True, blank=True)

    OPTIONS = (
        ('Done', 'Realizada'),
        ('Delayed', 'Atrasada'),
        ('Process', 'En proceso'),
        ('Pause', 'Pausada'),
        ('Reject', 'Rechazada'),
        ('Leaved', 'Abandonada')
    )

    status = models.CharField(max_length=15, choices=OPTIONS, default='Process')

    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, blank=True, related_name='work')

    user = models.ForeignKey(DeveloperProfile,
                             on_delete=models.SET_NULL,
                             null=True,
                             blank=True,
                             related_name='worker')

    def __str__(self):
        return self.name