"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import Link from "next/link";
import { getTeam, TeamDetail, MatchWithTournament } from "@/lib/api";

export default function TeamPage() {
  const params = useParams();
  const [team, setTeam] = useState<TeamDetail | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (params.id) {
      getTeam(Number(params.id))
        .then(setTeam)
        .catch((err) => setError(err.message))
        .finally(() => setLoading(false));
    }
  }, [params.id]);

  if (loading) {
    return (
      <div className="flex justify-center items-center min-h-[50vh]">
        <div className="text-xl text-slate-400">Loading team...</div>
      </div>
    );
  }

  if (error || !team) {
    return (
      <div className="flex justify-center items-center min-h-[50vh]">
        <div className="text-xl text-red-400">Error: {error || "Team not found"}</div>
      </div>
    );
  }

  // Calculate win/loss record
  const wins = team.matches.filter((m) => m.winner?.id === team.id).length;
  const losses = team.matches.length - wins;

  // Group matches by tournament
  const matchesByTournament = team.matches.reduce((acc, match) => {
    const key = match.tournament_id;
    if (!acc[key]) {
      acc[key] = {
        tournament_id: match.tournament_id,
        tournament_name: match.tournament_name,
        tournament_date: match.tournament_date,
        matches: [],
      };
    }
    acc[key].matches.push(match);
    return acc;
  }, {} as Record<number, { tournament_id: number; tournament_name: string; tournament_date: string; matches: MatchWithTournament[] }>);

  const tournamentResults = Object.values(matchesByTournament).sort(
    (a, b) => new Date(b.tournament_date).getTime() - new Date(a.tournament_date).getTime()
  );

  return (
    <div>
      <Link
        href="/"
        className="inline-flex items-center text-slate-400 hover:text-white mb-6 transition-colors"
      >
        ← Back to Home
      </Link>

      {/* Team Header */}
      <div className="bg-slate-800 rounded-lg p-6 border border-slate-700 mb-8">
        <h1 className="text-3xl font-bold text-white mb-4">{team.name}</h1>
        <div className="flex gap-6 text-slate-400">
          <div>
            <span className="text-green-400 font-semibold">{wins}</span> Wins
          </div>
          <div>
            <span className="text-red-400 font-semibold">{losses}</span> Losses
          </div>
          <div>
            <span className="text-blue-400 font-semibold">{team.players.length}</span> Players
          </div>
        </div>
      </div>

      {/* Players Section */}
      <h2 className="text-2xl font-bold text-white mb-4">Roster</h2>
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3 mb-8">
        {team.players.map((player) => (
          <div
            key={player.id}
            className="bg-slate-800 rounded-lg p-4 border border-slate-700"
          >
            <div className="text-lg font-semibold text-white">{player.name}</div>
            <div className="text-sm text-slate-400">{player.role}</div>
          </div>
        ))}
      </div>

      {/* Match History Section */}
      <h2 className="text-2xl font-bold text-white mb-4">Match History</h2>
      {tournamentResults.length === 0 ? (
        <div className="text-slate-400">No matches played yet.</div>
      ) : (
        <div className="space-y-6">
          {tournamentResults.map((tournamentGroup) => (
            <div
              key={tournamentGroup.tournament_id}
              className="bg-slate-800 rounded-lg border border-slate-700 overflow-hidden"
            >
              <Link
                href={`/tournament/${tournamentGroup.tournament_id}`}
                className="block bg-slate-750 p-4 border-b border-slate-700 hover:bg-slate-700 transition-colors"
              >
                <div className="flex justify-between items-center">
                  <h3 className="text-lg font-semibold text-white hover:text-blue-400 transition-colors">
                    {tournamentGroup.tournament_name}
                  </h3>
                  <span className="text-sm text-slate-400">
                    {new Date(tournamentGroup.tournament_date).toLocaleDateString("en-US", {
                      year: "numeric",
                      month: "short",
                      day: "numeric",
                    })}
                  </span>
                </div>
              </Link>
              <div className="divide-y divide-slate-700">
                {tournamentGroup.matches.map((match) => {
                  const isWin = match.winner?.id === team.id;
                  const opponent =
                    match.team1.id === team.id ? match.team2 : match.team1;

                  return (
                    <div
                      key={match.id}
                      className="p-4 flex items-center justify-between"
                    >
                      <div className="flex items-center gap-4">
                        <span
                          className={`text-sm font-semibold px-2 py-1 rounded ${
                            isWin
                              ? "bg-green-900 text-green-300"
                              : "bg-red-900 text-red-300"
                          }`}
                        >
                          {isWin ? "WIN" : "LOSS"}
                        </span>
                        <span className="text-slate-400">vs</span>
                        <Link
                          href={`/team/${opponent.id}`}
                          className="text-white hover:text-blue-400 transition-colors"
                        >
                          {opponent.name}
                        </Link>
                      </div>
                      <span className="text-sm text-slate-500">
                        {match.round_display}
                      </span>
                    </div>
                  );
                })}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
