from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.db import IntegrityError

from rest_framework.permissions import IsAuthenticated
from core.api.permissions import IsTeamOwnerByPropertyOrReadOnly,IsTeamMember
from teams.models import Team,TeamMembership
from teams.api.serializers import (TeamSerializer,
                                   AddMembersSerializer,
                                   RemoveMembersSerializer,
                                   RoleSerializer)

from django.shortcuts import get_object_or_404

class CreateTeamView(generics.CreateAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        try:
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        except IntegrityError:
            return Response(
                {"detail": "A team with this name already exists."},
                status=status.HTTP_400_BAD_REQUEST
            )

class RetreiveUpdateDestroyTeamView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = [IsAuthenticated,IsTeamOwnerByPropertyOrReadOnly,IsTeamMember]


class AddTeamMembersView(generics.UpdateAPIView):
    queryset = Team.objects.all()
    serializer_class = AddMembersSerializer
    permission_classes = [IsAuthenticated, IsTeamOwnerByPropertyOrReadOnly,IsTeamMember]
    
class RemoveTeamMembersView(generics.UpdateAPIView):
    queryset = Team.objects.all()
    serializer_class = RemoveMembersSerializer
    permission_classes = [IsAuthenticated, IsTeamOwnerByPropertyOrReadOnly,IsTeamMember]
    


class LeaveTeamView(APIView):
    permission_classes = [IsTeamMember, IsAuthenticated]

    def get_object(self, pk):
        return get_object_or_404(Team, pk=pk)

    def post(self, request, pk, *args, **kwargs):
        team = self.get_object(pk)

        if request.user == team.owner or request.user.is_superuser or request.user.is_staff:
            return Response({"detail": "Owner or Admin can't leave the team"}, status=status.HTTP_400_BAD_REQUEST)

        if request.user not in team.members.all():
            return Response({"message": "You are not a member of this team."}, status=status.HTTP_400_BAD_REQUEST)

        TeamMembership.objects.filter(team=team, user=request.user).delete()
        return Response({"message": "Successfully left the team."}, status=status.HTTP_200_OK)

    

class UpdateRoleView(generics.UpdateAPIView):
    queryset = TeamMembership.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [IsAuthenticated]


    def put(self, request, *args, **kwargs):
        username = request.data.get('username')
        try:
            user = get_user_model().objects.get(username=username)
            team_membership = TeamMembership.objects.get(user=user, team_id=int(self.kwargs.get('pk')))
        except TeamMembership.DoesNotExist:
            return Response({"error": "Invalid username or team ID."}, status=status.HTTP_400_BAD_REQUEST)

        if not self.can_change_maintainer_status(request.user):
            return Response({"error": "Not authorized to change maintainer status."}, status=status.HTTP_403_FORBIDDEN)

        team_membership.is_maintainer = request.data.get('is_maintainer', team_membership.is_maintainer)
        team_membership.save()

        serializer = self.get_serializer(team_membership)
        return Response(serializer.data)
    
    def can_change_maintainer_status(self, user):
        try:
            acc = get_user_model().objects.get(username=user.username)
            team_membership = TeamMembership.objects.get(user=acc, team_id=int(self.kwargs.get('pk')))
        except TeamMembership.DoesNotExist:
            return Response({"error": "User is not part of this team."}, status=status.HTTP_400_BAD_REQUEST)

        is_owner = team_membership.team.owner == acc
        is_superuser = acc.is_superuser
        is_staff = acc.is_staff
        is_maintainer = team_membership.is_maintainer

        return is_owner or is_superuser or is_staff or is_maintainer