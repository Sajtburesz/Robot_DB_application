from django.urls import include, path

from users.api.views import (AvatarSelectionView,
                             UserRetrieveUpdateDestroyView,
                             UserListView,
                             UserTeamsListView,
                             GetAdminStatusView,
                             ChangePasswordView,
                             CheckSessionView)


urlpatterns = [
    path('users/', UserListView.as_view(), name='user-list'),
    path('users/<str:username>/',UserRetrieveUpdateDestroyView.as_view(), name='user-detail'),
    path('users/<str:username>/teams/', UserTeamsListView.as_view(), name='user-teams-list'),
    path("avatar/change/", AvatarSelectionView.as_view(), name="avatar"),
    path("check-admin-status/", GetAdminStatusView.as_view(), name="admin-status"),
    path("change-password/", ChangePasswordView.as_view(), name="change-password"),
    path('check-session/', CheckSessionView.as_view(), name='check-session'),
]