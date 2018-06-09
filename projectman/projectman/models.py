from django.contrib.auth.models import Group, AbstractUser
from django.db import models
from django.core.exceptions import ObjectDoesNotExist


class User(AbstractUser):
    is_project_manager = models.BooleanField(default=False)
    is_developer = models.BooleanField(default=False)
    is_client = models.BooleanField(default=False)

    def get_projectmanager_profile(self):
        projectmanager_profile = None
        if hasattr(self, 'projectmanagerprofile'):
            projectmanager_profile = self.projectmanagerprofile
        return projectmanager_profile

    def get_developer_profile(self):
        developer_profile = None
        if hasattr(self, 'developerprofile'):
            developer_profile = self.developerprofile
        return developer_profile

    def get_client_profile(self):
        client_profile = None
        if hasattr(self, 'clientprofile'):
            client_profile = self.clientprofile
        return client_profile

    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)
        if self.is_project_manager:
            try:
                ProjectmanagerProfile.objects.get(user=self)
            except ObjectDoesNotExist:
                ProjectmanagerProfile.objects.create(user=self)
        else:
            try:
                user = ProjectmanagerProfile.objects.get(user=self)
            except ObjectDoesNotExist:
                pass
            else:
                ProjectmanagerProfile.delete(user)

        if self.is_developer:
            try:
                DeveloperProfile.objects.get(user=self)
            except ObjectDoesNotExist:
                DeveloperProfile.objects.create(user=self)
        else:
            try:
                user = DeveloperProfile.objects.get(user=self)
            except ObjectDoesNotExist:
                pass
            else:
                DeveloperProfile.delete(user)

        if self.is_client:
            try:
                ClientProfile.objects.get(user=self)
            except ObjectDoesNotExist:
                ClientProfile.objects.create(user=self)
        else:
            try:
                user = ClientProfile.objects.get(user=self)
            except ObjectDoesNotExist:
                pass
            else:
                ClientProfile.delete(user)

    class Meta:
        db_table = 'auth_user'


class ProjectmanagerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cellphone = models.CharField(max_length=10, default="")

    def __str__(self):
        return self.user.username


class DeveloperProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    github = models.CharField(max_length=60, default="")

    def __str__(self):
        return self.user.username


class ClientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cellphone = models.CharField(max_length=10, default="")

    def __str__(self):
        return self.user.username


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

    class Meta:
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
    state = models.IntegerField(choices=STATE, default=3)

    def __str__(self):
        return self.project.title + " - " + self.name

    def get_children(self):
        task = ChildTask.objects.filter(task=self)
        return task

    @property
    def json(self):
        return {
            "model": "projectman.task",
            "pk": self.pk,
            "fields": {
                'name': self.name,
                'project': str(self.project),
                'description': self.description,
                'requeriments': self.requeriments,
                'costs': self.costs,
                'estimated_target_date': str(self.estimated_target_date),
                'responsable': str(self.responsable),
                'priority': self.PRIORITY[self.priority - 1][1],
                'state': self.STATE[self.state - 1][1],
                'childs': self.task_child.count(),
            }

        }

    class Meta:
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


class ChildTask(models.Model):
    name = models.CharField(max_length=100)
    task = models.ForeignKey(Task, null=True, on_delete=models.SET_NULL, related_name='task_child')
    complete = models.BooleanField(default=False)

    def __str__(self):
        return self.name
