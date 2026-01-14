from rest_framework import generics

from .models import Tournament
from .serializers import TournamentDetailSerializer, TournamentListSerializer


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
