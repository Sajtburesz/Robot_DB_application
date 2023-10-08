from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, status

from users.api.serializers import UserDetailSelfSerializer,UserListSerializer,UserDetailOtherSerializer,UserAvatarSerializer
from users.models import User
from teams.api.serializers import UserTeamSerializer

from rest_framework.response import Response
from core.api.permissions import IsOwnerOrReadOnly

class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer


class UserRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
    lookup_field = 'username'

    def get_serializer_class(self):
        # If querying a specific user
        if self.request.method == 'GET' and self.kwargs.get('username'):
            # If the queried user matches the authenticated user
            if self.kwargs['username'] == self.request.user.username:
                return UserDetailSelfSerializer
            # If querying someone else's details
            else:
                return UserDetailOtherSerializer

        # Default to the self detail serializer for other actions (e.g., update)
        if self.kwargs['username'] == self.request.user.username:
            return UserDetailSelfSerializer
        else:
            return UserDetailOtherSerializer

    # Ensure that only the authenticated user can edit their own profile
    def update(self, request, *args, **kwargs):
        if kwargs['username'] != request.user.username:
            return Response({"detail": "You can only edit your own profile."}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        if kwargs['username'] != request.user.username:
            return Response({"detail": "You can only delete your own profile."}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)

class UserTeamsListView(generics.ListAPIView):
    serializer_class = UserTeamSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        owned_teams = user.owned_teams.all()
        member_teams_not_owned = user.member_teams().exclude(owner=user)
        return (owned_teams | member_teams_not_owned).order_by('name').distinct()

class AvatarUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = UserAvatarSerializer
    permission_classes = [IsOwnerOrReadOnly]  

    def get_queryset(self):
        return User.objects.all()

    def get_object(self):
        return get_object_or_404(User, username=self.kwargs['username'])

    def delete(self, request, *args, **kwargs):
        return Response({"detail": "Deletion not allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    