from rest_framework import permissions
from teams.models import TeamMembership

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
            return request.user.is_superuser or obj.owner == request.user
        

        if isinstance(obj, TeamMembership):
            team = obj.team
            membership = obj
        else:
            team = obj
            try:
                membership = TeamMembership.objects.get(user=request.user, team=team)
            except TeamMembership.DoesNotExist:
                membership = None

        # Check if the user is a maintainer
        is_maintainer = membership and membership.is_maintainer
        
        # Return True if the user is the owner, a maintainer, staff, or a superuser
        return team.owner == request.user or is_maintainer or request.user.is_superuser

    
class IsTeamMember(permissions.BasePermission):
    
    def has_object_permission(self, request, view, obj):
        return TeamMembership.objects.filter(team=obj, user=request.user).exists()

class IsOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.owner or request.user.is_superuser