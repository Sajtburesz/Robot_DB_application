from rest_framework import permissions
from teams.models import TeamMembership,Team
from robot_test_management.models import TestRun
from rest_framework.exceptions import PermissionDenied

class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj == request.user or request.user.is_superuser
    
class IsTeamOwnerByPropertyOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        if isinstance(obj, TeamMembership):
            team = obj.team
            membership = obj
        elif isinstance(obj,Team):
            team = obj
            try:
                membership = TeamMembership.objects.get(user=request.user, team=team)
            except TeamMembership.DoesNotExist:
                membership = None
        elif isinstance(obj,TestRun):
            team = Team.objects.get(id=obj.team_id)
            try:
                membership = TeamMembership.objects.get(user=request.user, team=team)
            except TeamMembership.DoesNotExist:
                membership = None
        else:
           return False
        
        if request.method == 'DELETE':
            return request.user.is_superuser or team.owner == request.user or request.user.is_staff

        maintainer = membership and membership.is_maintainer
        
        return team.owner == request.user or maintainer or request.user.is_superuser or request.user.is_staff

    
class IsTeamMember(permissions.BasePermission):
    
    def has_object_permission(self, request, view, obj):
        return TeamMembership.objects.filter(team=obj, user=request.user).exists()
    
class IsTeamMemberOfTeamProvidedInArgs(permissions.BasePermission):
    
    def has_permission(self, request, view):
        team_id = request.data.get('team')
        if not team_id:
            return False

        try:
            team = Team.objects.get(id=team_id)
        except Team.DoesNotExist:
            return False

        return TeamMembership.objects.filter(team=team, user=request.user).exists()


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
