from django.db import models


class Team(models.Model):
    """Represents a team that can participate in tournaments."""

    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Player(models.Model):
    """Represents a player on a team."""

    name = models.CharField(max_length=100)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="players")
    role = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.team.name})"

    class Meta:
        ordering = ["name"]


class Tournament(models.Model):
    """Represents a tournament."""

    TOURNAMENT_TYPES = [
        ("single_elimination", "Single Elimination"),
    ]

    name = models.CharField(max_length=200)
    tournament_type = models.CharField(
        max_length=50, choices=TOURNAMENT_TYPES, default="single_elimination"
    )
    date = models.DateField()
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-date"]


class Match(models.Model):
    """Represents a match in a tournament."""

    ROUND_NAMES = [
        ("finals", "Finals"),
        ("semifinals", "Semifinals"),
        ("quarterfinals", "Quarterfinals"),
        ("round_of_16", "Round of 16"),
    ]

    tournament = models.ForeignKey(
        Tournament, on_delete=models.CASCADE, related_name="matches"
    )
    round_name = models.CharField(max_length=50, choices=ROUND_NAMES)
    match_number = models.PositiveIntegerField()  # Order within the round
    team1 = models.ForeignKey(
        Team, on_delete=models.CASCADE, related_name="matches_as_team1"
    )
    team2 = models.ForeignKey(
        Team, on_delete=models.CASCADE, related_name="matches_as_team2"
    )
    winner = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name="matches_won",
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.tournament.name} - {self.get_round_name_display()} - {self.team1} vs {self.team2}"

    class Meta:
        ordering = ["tournament", "round_name", "match_number"]
        verbose_name_plural = "Matches"
