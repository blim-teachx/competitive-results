from django.urls import path

from .views import TournamentDetailView, TournamentListView

urlpatterns = [
    path("tournaments/", TournamentListView.as_view(), name="tournament-list"),
    path(
        "tournaments/<int:pk>/",
        TournamentDetailView.as_view(),
        name="tournament-detail",
    ),
]
