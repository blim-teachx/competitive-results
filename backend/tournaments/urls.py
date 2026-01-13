from django.urls import path

from .views import (
    TeamDetailView,
    TeamListView,
    TournamentDetailView,
    TournamentListView,
)

urlpatterns = [
    path("tournaments/", TournamentListView.as_view(), name="tournament-list"),
    path(
        "tournaments/<int:pk>/",
        TournamentDetailView.as_view(),
        name="tournament-detail",
    ),
    path("teams/", TeamListView.as_view(), name="team-list"),
    path("teams/<int:pk>/", TeamDetailView.as_view(), name="team-detail"),
]
