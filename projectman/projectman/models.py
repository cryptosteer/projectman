from django.contrib.auth.models import Group, AbstractUser
from django.db import models


class User(AbstractUser):
    is_project_manager = models.BooleanField(default=False)
    is_developer = models.BooleanField(default=False)
    is_client = models.BooleanField(default=True)

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
    STATE = (
        (1, 'Done'),
        (2, 'In-progess'),
        (3, 'To-do')
    )
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=500, default="", blank=True)
    project_manager = models.ForeignKey(ProjectmanagerProfile, blank=True, null=True, on_delete=models.CASCADE)
    client = models.ManyToManyField(ClientProfile)
    methodology = models.CharField(max_length=50)
    budget = models.BigIntegerField()
    price_hour_developer = models.FloatField(null=True)  # agregado
    hours_estimated = models.IntegerField(null=True)  # agregado
    resources = models.TextField()
    state = models.IntegerField(choices=STATE, null=True)
    time_start_real = models.DateField(blank=True, null=True)
    time_end_real = models.DateField(blank=True, null=True)
    time_start_estimated = models.DateField(blank=True, null=True)
    time_end_estimated = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):

       tasks = Task.objects.filter(project__id=self.id)

       res = False

       for a in tasks:
           if a.state == 1:
               pass
           else :
               res = True
               break
       if res ==False:
          super().save(*args, **kwargs)


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
    est_time = models.DateTimeField(blank=True, null=True)
    real_time = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.project.title + " - " + self.name

    def save(self, *args, **kwargs):
        if self.state == 1:
            self.real_time = datetime.datetime.now()
        super().save(*args, **kwargs)  # Call the "real" save() method.



    def __str__(self):
        return self.project.title + " - " + self.name


class Comment(models.Model):
    task = models.ForeignKey(Task, related_name="comment")
    owner = models.ForeignKey(User, related_name="owner")
    comment = models.TextField(max_length=300)
    keyword = models.CharField(max_length=20)
    date_created = models.DateField(auto_now_add=True)


class Log(models.Model):
    task = models.ForeignKey(Task, blank=True, null=True, on_delete=models.CASCADE)
    developer_profile = models.ForeignKey(DeveloperProfile, blank=True, null=True, on_delete=models.CASCADE)
    time_log = models.IntegerField(blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)


class Report(models.Model):
    project = models.OneToOneField(Project, null=True)
    # prueba=models.CharField(max_length=20, null=True)

