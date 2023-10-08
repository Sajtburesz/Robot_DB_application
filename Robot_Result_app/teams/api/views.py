from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model

from rest_framework.permissions import IsAuthenticated
from core.api.permissions import IsOwnerByPropertyOrReadOnly,IsTeamMember,IsOwnerOrAdmin

from teams.models import Team
from teams.api.serializers import TeamSerializer


class CreateTeamView(generics.CreateAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        team = serializer.save(owner=self.request.user)
        team.members.add(self.request.user)


class RetreiveUpdateDestroyTeamView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    lookup_field = 'pk'
    permission_classes = [IsAuthenticated,IsOwnerByPropertyOrReadOnly]


class LeaveTeamView(APIView):
    permission_classes = [IsTeamMember, IsAuthenticated]

    def get_object(self, pk):
        try:
            return Team.objects.get(pk=pk)
        except Team.DoesNotExist:
            return Response({"message": "Team does not exist."}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, pk, *args, **kwargs):
        team = self.get_object(pk)

        if request.user == team.owner:
            return Response({"detail": "Owner can't leave the team"}, status=status.HTTP_400_BAD_REQUEST)

        if request.user not in team.members.all():
            return Response({"message": "You are not a member of this team."}, status=status.HTTP_400_BAD_REQUEST)

        team.members.remove(request.user)
        return Response({"message": "Successfully left the team."}, status=status.HTTP_200_OK)
    

class ManageOwnerPermissionView(generics.UpdateAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

    def update(self, request, *args, **kwargs):
        team = self.get_object()
        
        # Get the action and username from the request data
        action = request.data.get('action', None)
        username = request.data.get('username', None)
        
        if not action or not username:
            return Response({"error": "Action or username not provided."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = get_user_model().objects.get(username=username)
        except get_user_model().DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        if action == "grant":
            if user not in team.members.all():
                return Response({"error": "User is not a member of the team."}, status=status.HTTP_400_BAD_REQUEST)
            team.members.add(user)  # Ensure the user remains a member after becoming an owner
        elif action == "revoke":
            if user == team.owner:
                return Response({"error": "Cannot revoke permissions from actual owner."}, status=status.HTTP_400_BAD_REQUEST)
            team.members.remove(user)
        else:
            return Response({"error": "Invalid action."}, status=status.HTTP_400_BAD_REQUEST)

        team.save()

        # Return the updated team details
        serializer = self.get_serializer(team)
        return Response(serializer.data)