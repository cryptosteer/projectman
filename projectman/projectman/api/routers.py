from rest_framework import routers

from projectman.api.viewset import ProjectViewSet, ClientProfileViewSet, DeveloperProfileViewSet
from .viewset import TaskViewSet, CommentViewSet, UserViewSet

router_project = routers.DefaultRouter()
router_project.register('task',TaskViewSet)
router_project.register('comment',CommentViewSet)
router_project.register('users',UserViewSet)
router_project.register('projects',ProjectViewSet)
router_project.register('client_profile',ClientProfileViewSet)
router_project.register('developers_profile',DeveloperProfileViewSet)