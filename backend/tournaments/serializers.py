from rest_framework import serializers

from .models import Match, Player, Team, Tournament


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ["id", "name"]


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ["id", "name", "role"]


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


class MatchWithTournamentSerializer(serializers.ModelSerializer):
    """Match serializer that includes tournament info for team results."""

    team1 = TeamSerializer(read_only=True)
    team2 = TeamSerializer(read_only=True)
    winner = TeamSerializer(read_only=True)
    round_display = serializers.CharField(
        source="get_round_name_display", read_only=True
    )
    tournament_id = serializers.IntegerField(source="tournament.id", read_only=True)
    tournament_name = serializers.CharField(source="tournament.name", read_only=True)
    tournament_date = serializers.DateField(source="tournament.date", read_only=True)

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
            "tournament_id",
            "tournament_name",
            "tournament_date",
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


class TeamListSerializer(serializers.ModelSerializer):
    """Serializer for team list view."""

    player_count = serializers.SerializerMethodField()

    class Meta:
        model = Team
        fields = ["id", "name", "player_count"]

    def get_player_count(self, obj):
        return obj.players.count()


class TeamDetailSerializer(serializers.ModelSerializer):
    """Serializer for team detail view with players and match history."""

    players = PlayerSerializer(many=True, read_only=True)
    matches = serializers.SerializerMethodField()

    class Meta:
        model = Team
        fields = ["id", "name", "players", "matches"]

    def get_matches(self, obj):
        from django.db.models import Q

        matches = (
            Match.objects.filter(Q(team1=obj) | Q(team2=obj))
            .select_related("tournament", "team1", "team2", "winner")
            .order_by("-tournament__date", "round_name")
        )
        return MatchWithTournamentSerializer(matches, many=True).data
