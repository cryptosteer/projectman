from django.contrib.auth.models import Group, AbstractUser, User
from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver




class User(AbstractUser):
    is_project_manager = models.BooleanField(default=False)
    is_developer = models.BooleanField(default=False)
    is_client = models.BooleanField(default=False)

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
        return '{} {}'.format(self.user.first_name, self.user.last_name)


class DeveloperProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    github = models.CharField(max_length=60, default="")

    def __str__(self):
        return '{} {}'.format(self.user.first_name, self.user.last_name)


class ClientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cellphone = models.CharField(max_length=10, default="")

    def __str__(self):
        return '{} {}'.format(self.user.first_name, self.user.last_name)


class Project(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=500, default="", blank=True)
    project_manager = models.OneToOneField(ProjectmanagerProfile, blank=True, null=True, on_delete=models.CASCADE)
    client = models.ManyToManyField(ClientProfile)
    methodology = models.CharField(max_length=50)
    budget = models.BigIntegerField()
    resources = models.TextField()
    time_start_real = models.DateField(blank=True, null=True)
    time_end_real = models.DateField(blank=True, null=True)
    time_start_estimated = models.DateField(blank=True, null=True)
    time_end_estimated = models.DateField(blank=True, null=True)
    position = models.PositiveSmallIntegerField("Position", null=False, default=0)

    class Meta:
        ordering = ['position']
        permissions = (
            ("view_project", "Can see projects"),
        )

    def __str__(self):
        return self.title


class Task(models.Model):
    PRIORITY = (
        (1, 'High'),
        (2, 'Medium'),
        (3, 'Low')
    )
    STATE = (
        (1, 'Done'),
        (2, 'In-progess'),
        (3, 'To-do')
    )
    name = models.CharField(max_length=100)
    project = models.ForeignKey(Project, blank=True, null=True, on_delete=models.CASCADE)
    description = models.TextField()
    requeriments = models.TextField()
    costs = models.BigIntegerField()
    estimated_target_date = models.DateField(blank=True, null=True)
    responsable = models.ForeignKey(DeveloperProfile, blank=True, null=True, on_delete=models.CASCADE)
    priority = models.IntegerField(choices=PRIORITY)
    state = models.IntegerField(choices=STATE)
    position = models.PositiveSmallIntegerField("Position", null=False, default=0)

    def __str__(self):
        return self.project.title + " - " + self.name

    @property
    def json(self):
        return {
            "model": "projectman.task",
            "pk": self.pk,
            "fields":{
                'name': self.name,
                'project': str(self.project),
                'description': self.description,
                'requeriments': self.requeriments,
                'costs': self.costs,
                'estimated_target_date': str(self.estimated_target_date),
                'responsable': str(self.responsable),
                'priority': self.PRIORITY[self.priority-1][1],
                'state': self.STATE[self.state-1][1],
            }

        }

    class Meta:
        ordering = ['position']
        permissions = (
            ("view_task", "Can see task"),
            ("change_status_task", "Can change status to task"),
        )


class Comment(models.Model):
    task = models.ForeignKey(Task, related_name="comment")
    owner = models.ForeignKey(User, related_name="owner")
    comment = models.TextField(max_length=300)
    keyword = models.CharField(max_length=20)
    date_created = models.DateField(auto_now_add=True)


@receiver(pre_delete, sender=Task, dispatch_uid='task_delete_signal')
def log_deleted_task(sender, instance, using, **kwargs):
    x = [e for e in Task.objects.all() if e.position > instance.position]
    if len(x) > 0:
        for i in x:
            i.position -= 1
            i.save()


@receiver(pre_delete, sender=Project, dispatch_uid='project_delete_signal')
def log_deleted_project(sender, instance, using, **kwargs):
    x = [e for e in Project.objects.all() if e.position > instance.position]
    if len(x) > 0:
        for i in x:
            i.position -= 1
            i.save()
