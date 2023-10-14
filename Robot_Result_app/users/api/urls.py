from django.urls import include, path

from users.api.views import (AvatarUpdateView,
                             UserRetrieveUpdateDestroyView,
                             UserListView,
                             UserTeamsListView)


urlpatterns = [
    path('users/', UserListView.as_view(), name='user-list'),
    path('users/<str:username>/',UserRetrieveUpdateDestroyView.as_view(), name='user-detail'),
    path('users/<str:username>/teams/', UserTeamsListView.as_view(), name='user-teams-list'),
    path("avatar/<str:username>/",
         AvatarUpdateView.as_view(),
         name="avatar"),

]