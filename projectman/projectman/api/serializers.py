from rest_framework import serializers
from projectman.models import Comment, Task, User, Project, ClientProfile, DeveloperProfile


class TaskSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Task
        fields = ('name',
                  'id',
                  'description',
                  'requeriments',
                  'costs',
                  'estimated_target_date',
                  'priority',
                  'state',
                  'position',
                  'project',
                  'comment',
                  'responsable')


class CommentSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Comment
        fields = '__all__'


class DeveloperProfileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DeveloperProfile
        fields = ('user', 'github')


class ProjectSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Project
        fields = ('title',
                  'description',
                  'methodology',
                  'budget',
                  'resources',
                  'time_start_real',
                  'time_end_real',
                  'time_start_estimated',
                  'time_end_estimated',
                  'position',)
        read_only_fields = ('project_manager', 'client',)


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('pk', 'username', 'first_name', 'last_name',
                  'email', 'is_project_manager', 'is_developer',
                  'is_client', 'image',)


class ClientProfileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ClientProfile
        fields = ('pk', 'user', 'cellphone')
