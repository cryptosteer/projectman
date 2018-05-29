from __future__ import unicode_literals
from django.contrib.auth.models import Group, AbstractUser
from django.db import models

# Create your models here.
# Hacer uno solo donde este la variable is_model
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

class DeveloperProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    github = models.CharField(max_length=60, default="")

class ClientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cellphone = models.CharField(max_length=10, default="")