from django.urls import path
from .views import (CreateTeamView,
                    RetreiveUpdateDestroyTeamView,
                    LeaveTeamView,
                    AddTeamMembersView,
                    RemoveTeamMembersView,
                    UpdateRoleView,)

urlpatterns = [
    path('teams/create/', CreateTeamView.as_view(), name='create-team'),
    path('teams/<int:pk>/', RetreiveUpdateDestroyTeamView.as_view(), name='manage-team'),
    path('teams/<int:pk>/leave/', LeaveTeamView.as_view(), name='leave-team'),
    path('teams/<int:pk>/add-members/', AddTeamMembersView.as_view(), name='add-members'),
    path('teams/<int:pk>/remove-members/', RemoveTeamMembersView.as_view(), name='remove-members'),
    path('teams/<int:pk>/roles/', UpdateRoleView.as_view(), name='roles'),
]
