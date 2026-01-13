from django.contrib import admin

from .models import Match, Team, Tournament


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ["name", "created_at"]
    search_fields = ["name"]


class MatchInline(admin.TabularInline):
    model = Match
    extra = 0


@admin.register(Tournament)
class TournamentAdmin(admin.ModelAdmin):
    list_display = ["name", "tournament_type", "date"]
    list_filter = ["tournament_type", "date"]
    search_fields = ["name"]
    inlines = [MatchInline]


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = [
        "tournament",
        "round_name",
        "match_number",
        "team1",
        "team2",
        "winner",
    ]
    list_filter = ["tournament", "round_name"]
