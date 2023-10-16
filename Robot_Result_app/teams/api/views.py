from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model

from rest_framework.permissions import IsAuthenticated
from core.api.permissions import IsOwnerByPropertyOrReadOnly,IsTeamMember,IsOwnerOrAdmin

from teams.models import Team,TeamMembership
from teams.api.serializers import (TeamSerializer,
                                   AddMembersSerializer,
                                   RemoveMembersSerializer,
                                   RoleSerializer)


class CreateTeamView(generics.CreateAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = [IsAuthenticated]



class RetreiveUpdateDestroyTeamView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = [IsAuthenticated,IsOwnerByPropertyOrReadOnly,IsTeamMember]


class AddTeamMembersView(generics.UpdateAPIView):
    queryset = Team.objects.all()
    serializer_class = AddMembersSerializer
    permission_classes = [IsAuthenticated, IsOwnerByPropertyOrReadOnly]
    
class RemoveTeamMembersView(generics.UpdateAPIView):
    queryset = Team.objects.all()
    serializer_class = RemoveMembersSerializer
    permission_classes = [IsAuthenticated, IsOwnerByPropertyOrReadOnly]
    


class LeaveTeamView(APIView):
    permission_classes = [IsTeamMember, IsAuthenticated]

    def get_object(self, pk):
        try:
            return Team.objects.get(pk=pk)
        except Team.DoesNotExist:
            return Response({"message": "Team does not exist."}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, pk, *args, **kwargs):
        team = self.get_object(pk)

        if request.user == team.owner or request.user.is_superuser:
            return Response({"detail": "Owner or Admin can't leave the team"}, status=status.HTTP_400_BAD_REQUEST)

        if request.user not in team.members.all():
            return Response({"message": "You are not a member of this team."}, status=status.HTTP_400_BAD_REQUEST)

        TeamMembership.objects.filter(team=team, user=request.user).delete()
        return Response({"message": "Successfully left the team."}, status=status.HTTP_200_OK)

    

class UpdateRoleView(generics.UpdateAPIView):
    queryset = TeamMembership.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [IsAuthenticated, IsOwnerByPropertyOrReadOnly]


    def update(self, request, *args, **kwargs):
        username = request.data.get('username')
        print(username)
        try:
            user = get_user_model().objects.get(username=username)
            team_membership = TeamMembership.objects.get(user=user, team_id=int(self.kwargs.get('pk')))
        except TeamMembership.DoesNotExist:
            return Response({"error": "Invalid username or team ID."}, status=status.HTTP_400_BAD_REQUEST)

        # Update the is_maintainer attribute
        team_membership.is_maintainer = request.data.get('is_maintainer', team_membership.is_maintainer)
        team_membership.save()

        # Return the updated team membership details
        serializer = self.get_serializer(team_membership)
        return Response(serializer.data)