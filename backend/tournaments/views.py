from rest_framework import generics

from .models import Team, Tournament
from .serializers import (
    TeamDetailSerializer,
    TeamListSerializer,
    TournamentDetailSerializer,
    TournamentListSerializer,
)


class TournamentListView(generics.ListAPIView):
    """List all tournaments."""

    queryset = Tournament.objects.all()
    serializer_class = TournamentListSerializer


class TournamentDetailView(generics.RetrieveAPIView):
    """Retrieve a single tournament with all its matches."""

    queryset = Tournament.objects.prefetch_related(
        "matches__team1", "matches__team2", "matches__winner"
    )
    serializer_class = TournamentDetailSerializer


class TeamListView(generics.ListAPIView):
    """List all teams."""

    queryset = Team.objects.prefetch_related("players").order_by("name")
    serializer_class = TeamListSerializer


class TeamDetailView(generics.RetrieveAPIView):
    """Retrieve a single team with players and match history."""

    queryset = Team.objects.prefetch_related("players")
    serializer_class = TeamDetailSerializer
