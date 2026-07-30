from rest_framework.permissions import BasePermission, SAFE_METHODS
from workspace.models import Task, User, Project

class IsYourTask(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser: return True
        if request.user in obj.project.members.all():
            if obj.created_by == request.user: return True
        if request.method in SAFE_METHODS:
            return obj.project.owner.pk == request.user.pk or request.user in obj.project.members.all() 
        return obj.project.owner.pk == request.user.pk
    
class IsOwnerOrMember(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser: return True
        if request.method in SAFE_METHODS:
            return obj.owner.pk == request.user.pk or request.user in obj.members.all()
        return obj.owner.pk == request.user.pk
    
class IsSuperAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user == User.objects.filter(is_superuser=1)

