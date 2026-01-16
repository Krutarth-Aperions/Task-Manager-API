from rest_framework.permissions import BasePermission
from workspace.models import Task, User, Project

class IsYourTask(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.project.owner.pk == request.user.pk
    
class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner.pk == request.user.pk
    
class IsSuperAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user == User.objects.filter(is_superuser=1)

