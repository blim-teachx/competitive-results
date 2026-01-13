from datetime import date

from django.core.management.base import BaseCommand

from tournaments.models import Match, Player, Team, Tournament


class Command(BaseCommand):
    help = "Seeds the database with example tournaments and teams"

    def handle(self, *args, **options):
        self.stdout.write("Seeding database...")

        # Create teams that appear across multiple tournaments with their players
        teams_data = {
            "Thunder Hawks": [
                ("Alex Storm", "Captain"),
                ("Jordan Blaze", "Support"),
                ("Casey Thunder", "DPS"),
                ("Riley Hawk", "Tank"),
                ("Morgan Swift", "Flex"),
            ],
            "Storm Breakers": [
                ("Sam Lightning", "Captain"),
                ("Taylor Wave", "Support"),
                ("Jamie Gale", "DPS"),
                ("Drew Tempest", "Tank"),
                ("Quinn Surge", "Flex"),
            ],
            "Phoenix Rising": [
                ("Avery Flame", "Captain"),
                ("Blake Ember", "Support"),
                ("Charlie Ash", "DPS"),
                ("Dana Spark", "Tank"),
                ("Ellis Fire", "Flex"),
            ],
            "Iron Wolves": [
                ("Finn Steel", "Captain"),
                ("Gray Fang", "Support"),
                ("Harper Claw", "DPS"),
                ("Indigo Howl", "Tank"),
                ("Jesse Pack", "Flex"),
            ],
            "Shadow Knights": [
                ("Kai Shade", "Captain"),
                ("Lee Dusk", "Support"),
                ("Max Shadow", "DPS"),
                ("Nico Dark", "Tank"),
                ("Oakley Knight", "Flex"),
            ],
            "Golden Eagles": [
                ("Parker Gold", "Captain"),
                ("Quinn Talon", "Support"),
                ("Reese Soar", "DPS"),
                ("Sage Wing", "Tank"),
                ("Tatum Sky", "Flex"),
            ],
            "Cyber Dragons": [
                ("Uma Circuit", "Captain"),
                ("Val Byte", "Support"),
                ("Winter Code", "DPS"),
                ("Xen Data", "Tank"),
                ("Yuri Pixel", "Flex"),
            ],
            "Frost Giants": [
                ("Zara Ice", "Captain"),
                ("Atlas Frost", "Support"),
                ("Blair Glacier", "DPS"),
                ("Coby Snow", "Tank"),
                ("Devon Chill", "Flex"),
            ],
        }

        teams = {}
        for team_name, players in teams_data.items():
            team, created = Team.objects.get_or_create(name=team_name)
            teams[team_name] = team
            if created:
                self.stdout.write(f"  Created team: {team_name}")
                # Add players to the team
                for player_name, role in players:
                    Player.objects.create(name=player_name, team=team, role=role)
                    self.stdout.write(f"    Added player: {player_name} ({role})")

        # Tournament 1: Round of 8 (Quarterfinals -> Semifinals -> Finals)
        tournament1, created = Tournament.objects.get_or_create(
            name="Winter Championship 2024",
            defaults={
                "tournament_type": "single_elimination",
                "date": date(2024, 1, 15),
                "description": "The premier winter esports championship featuring 8 top teams.",
            },
        )
        if created:
            self.stdout.write(f"  Created tournament: {tournament1.name}")

            # Quarterfinals
            qf1 = Match.objects.create(
                tournament=tournament1,
                round_name="quarterfinals",
                match_number=1,
                team1=teams["Thunder Hawks"],
                team2=teams["Storm Breakers"],
                winner=teams["Thunder Hawks"],
            )
            qf2 = Match.objects.create(
                tournament=tournament1,
                round_name="quarterfinals",
                match_number=2,
                team1=teams["Phoenix Rising"],
                team2=teams["Iron Wolves"],
                winner=teams["Phoenix Rising"],
            )
            qf3 = Match.objects.create(
                tournament=tournament1,
                round_name="quarterfinals",
                match_number=3,
                team1=teams["Shadow Knights"],
                team2=teams["Golden Eagles"],
                winner=teams["Golden Eagles"],
            )
            qf4 = Match.objects.create(
                tournament=tournament1,
                round_name="quarterfinals",
                match_number=4,
                team1=teams["Cyber Dragons"],
                team2=teams["Frost Giants"],
                winner=teams["Cyber Dragons"],
            )

            # Semifinals
            sf1 = Match.objects.create(
                tournament=tournament1,
                round_name="semifinals",
                match_number=1,
                team1=teams["Thunder Hawks"],
                team2=teams["Phoenix Rising"],
                winner=teams["Thunder Hawks"],
            )
            sf2 = Match.objects.create(
                tournament=tournament1,
                round_name="semifinals",
                match_number=2,
                team1=teams["Golden Eagles"],
                team2=teams["Cyber Dragons"],
                winner=teams["Cyber Dragons"],
            )

            # Finals
            Match.objects.create(
                tournament=tournament1,
                round_name="finals",
                match_number=1,
                team1=teams["Thunder Hawks"],
                team2=teams["Cyber Dragons"],
                winner=teams["Thunder Hawks"],
            )

        # Tournament 2: Round of 4 (Semifinals -> Finals)
        tournament2, created = Tournament.objects.get_or_create(
            name="Spring Invitational 2024",
            defaults={
                "tournament_type": "single_elimination",
                "date": date(2024, 4, 20),
                "description": "An exclusive invitational tournament with 4 elite teams.",
            },
        )
        if created:
            self.stdout.write(f"  Created tournament: {tournament2.name}")

            # Semifinals
            sf1 = Match.objects.create(
                tournament=tournament2,
                round_name="semifinals",
                match_number=1,
                team1=teams["Thunder Hawks"],
                team2=teams["Iron Wolves"],
                winner=teams["Iron Wolves"],
            )
            sf2 = Match.objects.create(
                tournament=tournament2,
                round_name="semifinals",
                match_number=2,
                team1=teams["Phoenix Rising"],
                team2=teams["Frost Giants"],
                winner=teams["Phoenix Rising"],
            )

            # Finals
            Match.objects.create(
                tournament=tournament2,
                round_name="finals",
                match_number=1,
                team1=teams["Iron Wolves"],
                team2=teams["Phoenix Rising"],
                winner=teams["Phoenix Rising"],
            )

        # Tournament 3: Another Round of 8
        tournament3, created = Tournament.objects.get_or_create(
            name="Summer Grand Prix 2024",
            defaults={
                "tournament_type": "single_elimination",
                "date": date(2024, 7, 10),
                "description": "The biggest summer tournament with teams from around the world.",
            },
        )
        if created:
            self.stdout.write(f"  Created tournament: {tournament3.name}")

            # Quarterfinals
            Match.objects.create(
                tournament=tournament3,
                round_name="quarterfinals",
                match_number=1,
                team1=teams["Iron Wolves"],
                team2=teams["Thunder Hawks"],
                winner=teams["Iron Wolves"],
            )
            Match.objects.create(
                tournament=tournament3,
                round_name="quarterfinals",
                match_number=2,
                team1=teams["Frost Giants"],
                team2=teams["Shadow Knights"],
                winner=teams["Frost Giants"],
            )
            Match.objects.create(
                tournament=tournament3,
                round_name="quarterfinals",
                match_number=3,
                team1=teams["Golden Eagles"],
                team2=teams["Phoenix Rising"],
                winner=teams["Phoenix Rising"],
            )
            Match.objects.create(
                tournament=tournament3,
                round_name="quarterfinals",
                match_number=4,
                team1=teams["Storm Breakers"],
                team2=teams["Cyber Dragons"],
                winner=teams["Storm Breakers"],
            )

            # Semifinals
            Match.objects.create(
                tournament=tournament3,
                round_name="semifinals",
                match_number=1,
                team1=teams["Iron Wolves"],
                team2=teams["Frost Giants"],
                winner=teams["Iron Wolves"],
            )
            Match.objects.create(
                tournament=tournament3,
                round_name="semifinals",
                match_number=2,
                team1=teams["Phoenix Rising"],
                team2=teams["Storm Breakers"],
                winner=teams["Phoenix Rising"],
            )

            # Finals
            Match.objects.create(
                tournament=tournament3,
                round_name="finals",
                match_number=1,
                team1=teams["Iron Wolves"],
                team2=teams["Phoenix Rising"],
                winner=teams["Iron Wolves"],
            )

        # Tournament 4: Another Round of 4
        tournament4, created = Tournament.objects.get_or_create(
            name="Fall Classic 2024",
            defaults={
                "tournament_type": "single_elimination",
                "date": date(2024, 10, 5),
                "description": "The autumn showdown between the top 4 ranked teams.",
            },
        )
        if created:
            self.stdout.write(f"  Created tournament: {tournament4.name}")

            # Semifinals
            Match.objects.create(
                tournament=tournament4,
                round_name="semifinals",
                match_number=1,
                team1=teams["Cyber Dragons"],
                team2=teams["Golden Eagles"],
                winner=teams["Cyber Dragons"],
            )
            Match.objects.create(
                tournament=tournament4,
                round_name="semifinals",
                match_number=2,
                team1=teams["Shadow Knights"],
                team2=teams["Storm Breakers"],
                winner=teams["Shadow Knights"],
            )

            # Finals
            Match.objects.create(
                tournament=tournament4,
                round_name="finals",
                match_number=1,
                team1=teams["Cyber Dragons"],
                team2=teams["Shadow Knights"],
                winner=teams["Shadow Knights"],
            )

        self.stdout.write(self.style.SUCCESS("Database seeded successfully!"))
