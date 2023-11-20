from rest_framework import permissions
from teams.models import TeamMembership
from rest_framework.exceptions import PermissionDenied

class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj == request.user
    
class IsTeamOwnerByPropertyOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        if request.method == 'DELETE':
            return request.user.is_superuser or obj.owner == request.user or request.user.is_staff
        

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
        return team.owner == request.user or is_maintainer or request.user.is_superuser or request.user.is_staff

    
class IsTeamMember(permissions.BasePermission):
    
    def has_object_permission(self, request, view, obj):
        return TeamMembership.objects.filter(team=obj, user=request.user).exists()

class IsOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.owner or request.user.is_superuser or request.user.is_staff
    
class IsAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_superuser or request.user.is_staff
    

class IsTeamMemberOfRelatedTeam(permissions.BasePermission):

    def has_permission(self, request, view):
        team_pk = view.kwargs.get('teamId')
        
        if not TeamMembership.objects.filter(team_id=team_pk, user=request.user).exists():
            raise PermissionDenied(detail="You are not a member of the specified team.")
        
        return True
    
    
class IsCommentAuthorOrAdmin(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user or request.user.is_superuser or request.user.is_staff
