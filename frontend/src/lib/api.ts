const API_BASE_URL = "http://localhost:8000/api";

export interface Team {
  id: number;
  name: string;
}

export interface TeamListItem {
  id: number;
  name: string;
  player_count: number;
}

export interface Player {
  id: number;
  name: string;
  role: string;
}

export interface Match {
  id: number;
  round_name: string;
  round_display: string;
  match_number: number;
  team1: Team;
  team2: Team;
  winner: Team | null;
}

export interface MatchWithTournament extends Match {
  tournament_id: number;
  tournament_name: string;
  tournament_date: string;
}

export interface Tournament {
  id: number;
  name: string;
  tournament_type: string;
  date: string;
  description: string;
}

export interface TournamentDetail extends Tournament {
  matches: Match[];
}

export interface TeamDetail {
  id: number;
  name: string;
  players: Player[];
  matches: MatchWithTournament[];
}

export async function getTournaments(): Promise<Tournament[]> {
  const response = await fetch(`${API_BASE_URL}/tournaments/`);
  if (!response.ok) {
    throw new Error("Failed to fetch tournaments");
  }
  return response.json();
}

export async function getTournament(id: number): Promise<TournamentDetail> {
  const response = await fetch(`${API_BASE_URL}/tournaments/${id}/`);
  if (!response.ok) {
    throw new Error("Failed to fetch tournament");
  }
  return response.json();
}

export async function getTeams(): Promise<TeamListItem[]> {
  const response = await fetch(`${API_BASE_URL}/teams/`);
  if (!response.ok) {
    throw new Error("Failed to fetch teams");
  }
  return response.json();
}

export async function getTeam(id: number): Promise<TeamDetail> {
  const response = await fetch(`${API_BASE_URL}/teams/${id}/`);
  if (!response.ok) {
    throw new Error("Failed to fetch team");
  }
  return response.json();
}
