from django.contrib.auth.models import User,Group
from django.db import models

# Create your models here.
# Hacer uno solo donde este la variable is_model
class Project_Manager(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user.groups.add(grupo)

class Developer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)