const API_BASE_URL = 'http://localhost:8000/api';

export interface Team {
  id: number;
  name: string;
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

export async function getTournaments(): Promise<Tournament[]> {
  const response = await fetch(`${API_BASE_URL}/tournaments/`);
  if (!response.ok) {
    throw new Error('Failed to fetch tournaments');
  }
  return response.json();
}

export async function getTournament(id: number): Promise<TournamentDetail> {
  const response = await fetch(`${API_BASE_URL}/tournaments/${id}/`);
  if (!response.ok) {
    throw new Error('Failed to fetch tournament');
  }
  return response.json();
}
