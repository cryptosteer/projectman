import datetime

from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from .users import User, ProjectmanagerProfile, ClientProfile, DeveloperProfile
from django.db.models.signals import pre_delete
from django.dispatch import receiver


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
    resources = models.TextField()
    time_start_real = models.DateField(blank=True, null=True)
    time_end_real = models.DateField(blank=True, null=True)
    time_start_estimated = models.DateField(blank=True, null=True)
    time_end_estimated = models.DateField(blank=True, null=True)
    position = models.PositiveSmallIntegerField("Position", null=False, default=0)
    state = models.IntegerField(choices=STATE, null=True)

    class Meta:
        ordering = ['position']
        permissions = (
            ("view_project", "Can see projects"),
        )

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        try:
            Project.objects.get(id=self.id)

            tasks = Task.objects.filter(project__id=self.id)

            res = False

            for a in tasks:
                if a.state == 1:
                    pass
                else:
                    res = True
                    break

            if res == False:
                if len(tasks) != 0:
                    self.time_end_real = datetime.datetime.now()
                    super().save(*args, **kwargs)
        except ObjectDoesNotExist:
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
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    description = models.TextField()
    requeriments = models.TextField()
    costs = models.BigIntegerField()
    estimated_target_date = models.DateField(blank=True, null=True)
    responsable = models.ForeignKey(DeveloperProfile, blank=True, null=True, on_delete=models.CASCADE)
    priority = models.IntegerField(choices=PRIORITY)
    state = models.IntegerField(choices=STATE)
    position = models.PositiveSmallIntegerField("Position", null=False, default=0)
    est_time = models.DateTimeField(blank=True, null=True)
    real_time = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.project.title + " - " + self.name

    def save(self, *args, **kwargs):
        if self.state == 1:
            self.real_time = datetime.datetime.now()
        super().save(*args, **kwargs)  # Call the "real" save() method.

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


class Log(models.Model):
    task = models.ForeignKey(Task, blank=True, null=True, on_delete=models.CASCADE)
    developer_profile = models.ForeignKey(DeveloperProfile, blank=True, null=True, on_delete=models.CASCADE)
    time_log = models.IntegerField(blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)

    def save(self, *args, **kwargs):
        self.date = datetime.datetime.now()
        super().save(*args, **kwargs)
