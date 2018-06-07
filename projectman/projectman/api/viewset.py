from rest_framework import viewsets
from .serializers import TaskSerializer, CommentSerializer, UserSerializer, ProjectSerializer, ClientProfileSerializer, \
    DeveloperProfileSerializer
from projectman.models import Task, Comment, User, Project, ClientProfile, DeveloperProfile


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class ClientProfileViewSet(viewsets.ModelViewSet):
    queryset = ClientProfile.objects.all()
    serializer_class = ClientProfileSerializer

class DeveloperProfileViewSet(viewsets.ModelViewSet):
    queryset = DeveloperProfile.objects.all()
    serializer_class = DeveloperProfileSerializer