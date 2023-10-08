from django.urls import path
from .views import (CreateTeamView,
                    RetreiveUpdateDestroyTeamView,
                    LeaveTeamView)

urlpatterns = [
    path('teams/create/', CreateTeamView.as_view(), name='create-team'),
    path('teams/<int:pk>/', RetreiveUpdateDestroyTeamView.as_view(), name='manage-team'),
    path('teams/<int:pk>/leave/', LeaveTeamView.as_view(), name='leave-team'),

]
