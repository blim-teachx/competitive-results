from rest_framework import serializers

from .models import Match, Team, Tournament


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ["id", "name"]


class MatchSerializer(serializers.ModelSerializer):
    team1 = TeamSerializer(read_only=True)
    team2 = TeamSerializer(read_only=True)
    winner = TeamSerializer(read_only=True)
    round_display = serializers.CharField(
        source="get_round_name_display", read_only=True
    )

    class Meta:
        model = Match
        fields = [
            "id",
            "round_name",
            "round_display",
            "match_number",
            "team1",
            "team2",
            "winner",
        ]


class TournamentListSerializer(serializers.ModelSerializer):
    """Serializer for tournament list view."""

    class Meta:
        model = Tournament
        fields = ["id", "name", "tournament_type", "date", "description"]


class TournamentDetailSerializer(serializers.ModelSerializer):
    """Serializer for tournament detail view with matches."""

    matches = MatchSerializer(many=True, read_only=True)

    class Meta:
        model = Tournament
        fields = ["id", "name", "tournament_type", "date", "description", "matches"]
