from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied

class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj == request.user
    
class IsOwnerByPropertyOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        if request.method == 'DELETE':
            return request.user.is_staff or request.user.is_superuser or obj.owner == request.user

        return obj.owner == request.user 
    # or request.user in obj.owner_permissions.all()
    
class IsTeamMember(permissions.BasePermission):
    
    def has_object_permission(self, request, view, obj):
        return request.user in obj.members.all()
    
class IsOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.owner or request.user.is_staff or request.user.is_superuser