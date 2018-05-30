from django.db import models
from projectman.models import ProjectmanagerProfile as Project_Man, DeveloperProfile as Developer


# Create your models here.
class Project(models.Model):
    name = models.CharField(max_length=20, null=False, blank=False)
    description = models.TextField(null=False, blank=False)
    init_date = models.DateTimeField(auto_now_add=True, editable=False, blank=True)
    finish_date = models.DateField(null=True, blank=True)

    project_man = models.OneToOneField(Project_Man,
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
        return Task.objects.filter(project=self, status=    'Process').count()

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

    user = models.ForeignKey(Developer,
                             on_delete=models.SET_NULL,
                             null=True,
                             blank=True,
                             related_name='worker')

    def __str__(self):
        return self.name