from django.utils import timezone
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from django.core.exceptions import ValidationError
from rest_framework import generics, status, views
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from django.contrib.sessions.models import Session
from config import settings

from users.api.serializers import UserDetailSelfSerializer,UserListSerializer,UserDetailOtherSerializer
from users.models import User
from teams.api.serializers import UserTeamSerializer
from users.api.filters import UserFilter

from rest_framework.response import Response
from core.api.permissions import IsOwnerOrReadOnly,IsAdmin

from teams.models import Team,TeamMembership
from django.db import transaction

class UserListView(generics.ListAPIView):
    queryset = User.objects.all().order_by('username')
    serializer_class = UserListSerializer
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_class = UserFilter

class UserRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    lookup_field = 'username'

    def get_serializer_class(self):
        # If querying a specific user
        if self.request.method == 'GET' and self.kwargs.get('username'):
            # If the queried user matches the authenticated user
            if self.kwargs.get('username') == self.request.user.username:
                return UserDetailSelfSerializer
            # If querying someone else's details
            else:
                return UserDetailOtherSerializer

        # Default to the self detail serializer for other actions (e.g., update)
        if self.kwargs.get('username') == self.request.user.username:
            return UserDetailSelfSerializer
        else:
            return UserDetailOtherSerializer

    # Ensure that only the authenticated user can edit their own profile
    def update(self, request, *args, **kwargs):
        if self.kwargs.get('username') != request.user.username:
            return Response({"detail": "You can only edit your own profile."}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        if request.user.is_staff or request.user.is_superuser:
            return super().destroy(request, *args, **kwargs)
        if self.kwargs.get('username') != request.user.username:
            return Response({"detail": "You can only delete your own profile."}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)

class UserTeamsListView(generics.ListAPIView):
    serializer_class = UserTeamSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        owned_teams = user.owned_teams.all()
        member_teams_not_owned = user.member_teams().exclude(owner=user)
        return (owned_teams | member_teams_not_owned).order_by('id').distinct()


class AvatarSelectionView(views.APIView):
    def get(self, request, *args, **kwargs):
        avatars = ['avatar1.png', 'avatar2.png', 'avatar3.png', 'avatar4.png','default.png']
        return Response({'avatars': avatars}, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        user = request.user
        avatar_choice = request.data.get('avatar')

        if avatar_choice in ['avatar1.png', 'avatar2.png', 'avatar3.png','avatar4.png', 'default.png']:
            user.avatar = avatar_choice
            user.save()
            return Response({'message': 'Avatar updated successfully.'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid avatar choice.'}, status=status.HTTP_400_BAD_REQUEST)
    
class GetAdminStatusView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            'is_superuser': request.user.is_superuser,
            'is_staff': request.user.is_staff,
        })
    
class GetSelfUsernameView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Get the username of the authenticated user
        username = request.user.username
        return Response({"username": username})
    
class ResetPasswordView(views.APIView):
    permission_classes = [IsAuthenticated,IsAdmin]

    def post(self, request, *args, **kwargs):
        try:
            if not request.user.is_superuser or not request.user.is_staff:
                return Response({'status': 'error','message': 'Only admins can perform this action.'}, status=status.HTTP_403_FORBIDDEN)
            username = request.data.get('username')
            new_password = request.data.get('new_password')

            if not username or not new_password:
                return Response({'status': 'error','message': 'Username and new password are required.'}, status=status.HTTP_400_BAD_REQUEST)

            user = User.objects.get(username=username)
            user.password = make_password(new_password)
            user.save()
            self.logout_user_everywhere(user)

            return Response({'status': 'success','message': 'Password successfully reset.'}, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({'status': 'error','message': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({'status': 'error','message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def logout_user_everywhere(self, user):
        user_sessions = Session.objects.filter(expire_date__gte=timezone.now())
        for session in user_sessions:
            session_data = session.get_decoded()
            if session_data.get('_auth_user_id', None) == str(user.id):
                session.delete()

class ManageAdminRightsAPIView(views.APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        try:
            with transaction.atomic():
                user = User.objects.get(username=username)

                if user.is_superuser:
                    raise PermissionDenied('Cannot modify superuser.')
                
                if user.is_staff:
                    user.is_staff = False
                    user.save()
                    return Response({'status': 'success', 'message': 'Admin rights revoked.'}, status=status.HTTP_200_OK)

                user.is_staff = True
                user.save()

                # Add the user to every team
                self.add_user_to_all_teams(user)

            return Response({'status': 'success', 'message': 'Admin rights granted.'}, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({'status': 'error', 'message': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
        except PermissionDenied as e:
            return Response({'status': 'error', 'message': str(e)}, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            return Response({'status': 'error', 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def add_user_to_all_teams(self, user):
        memberships_to_create = []

        existing_memberships = TeamMembership.objects.filter(user=user).values_list('team_id', flat=True)
        teams_to_add = Team.objects.exclude(id__in=existing_memberships)

        for team in teams_to_add:
            memberships_to_create.append(TeamMembership(team=team, user=user))

        TeamMembership.objects.bulk_create(memberships_to_create)


class ChangePasswordView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")

        if not user.check_password(old_password):
            return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)

        try:
            validate_password(new_password, user)
        except ValidationError as e:
            return Response({"new_password": list(e.messages)}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()
        return Response({"status": "success"}, status=status.HTTP_200_OK)