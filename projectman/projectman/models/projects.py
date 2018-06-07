from django.db import models
from .users import User, ProjectmanagerProfile, ClientProfile, DeveloperProfile


class Project(models.Model):
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
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    description = models.TextField()
    requeriments = models.TextField()
    costs = models.BigIntegerField()
    estimated_target_date = models.DateField(blank=True, null=True)
    responsable = models.ForeignKey(DeveloperProfile, blank=True, null=True, on_delete=models.CASCADE)
    priority = models.IntegerField(choices=PRIORITY)
    state = models.IntegerField(choices=STATE)

    def __str__(self):
        return self.project.title + " - " + self.name

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


class Comment(models.Model):
    task = models.ForeignKey(Task, related_name="comment")
    owner = models.ForeignKey(User, related_name="owner")
    comment = models.TextField(max_length=300)
    keyword = models.CharField(max_length=20)
    date_created = models.DateField(auto_now_add=True)
