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
        return str(self.user) + "'s Project manager profile"


class DeveloperProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    github = models.CharField(max_length=60, default="")

    def __str__(self):
        return str(self.user) + "'s Developer profile"


class ClientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cellphone = models.CharField(max_length=10, default="")

    def __str__(self):
        return str(self.user) + "'s Client profile"


class Project(models.Model):
    title = models.CharField(max_length=64,default="")
    description = models.TextField(max_length=500,default="")
    start_day = models.DateField()
    end_day = models.DateField()

    def __str__(self):
        return self.title

    # def __repr__(self):
    #     return 'Project(title={0}, ' \
    #            'description={1},' \
    #            ' start_day={2},' \
    #            ' end_day={3})'.format(self.title, self.description, self.start_day, self.end_day)


class Task(models.Model):
    PRIORITY = (
        (1, 'High'),
        (2, 'Medium'),
        (3, 'Low')
    )
    STATE = (
        (1, 'Done'),
        (2, 'Delayed'),
        (3, 'In-progess'),
        (4, 'To-do')
    )
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    target_day = models.DateField()
    description = models.CharField(max_length=100, default="")
    priority = models.IntegerField(choices=PRIORITY,default=2)
    state = models.IntegerField(choices=STATE,default=4)

    def __str__(self):
        return self.description + " - " + self.project.title



# * to * en relación task - developerprofile
# 1 to * en relación projectmanagerprofile - project
# 1 to * en relación clientprofile - project