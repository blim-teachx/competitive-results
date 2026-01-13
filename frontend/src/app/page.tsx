"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { getTournaments, getTeams, Tournament, TeamListItem } from "@/lib/api";

export default function Home() {
  const [tournaments, setTournaments] = useState<Tournament[]>([]);
  const [teams, setTeams] = useState<TeamListItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    Promise.all([getTournaments(), getTeams()])
      .then(([tournamentsData, teamsData]) => {
        setTournaments(tournamentsData);
        setTeams(teamsData);
      })
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <div className="flex justify-center items-center min-h-[50vh]">
        <div className="text-xl text-slate-400">Loading...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex justify-center items-center min-h-[50vh]">
        <div className="text-xl text-red-400">Error: {error}</div>
      </div>
    );
  }

  return (
    <div>
      {/* Tournaments Section */}
      <h1 className="text-3xl font-bold mb-8 text-white">Tournaments</h1>

      <div className="grid gap-6 md:grid-cols-2 mb-12">
        {tournaments.map((tournament) => (
          <Link
            key={tournament.id}
            href={`/tournament/${tournament.id}`}
            className="block bg-slate-800 rounded-lg p-6 border border-slate-700 hover:border-blue-500 hover:bg-slate-750 transition-all duration-200 group"
          >
            <div className="flex justify-between items-start mb-3">
              <h2 className="text-xl font-semibold text-white group-hover:text-blue-400 transition-colors">
                {tournament.name}
              </h2>
              <span className="text-sm bg-blue-600 text-white px-2 py-1 rounded">
                {tournament.tournament_type === "single_elimination"
                  ? "Single Elim"
                  : tournament.tournament_type}
              </span>
            </div>
            <p className="text-slate-400 mb-3">{tournament.description}</p>
            <div className="text-sm text-slate-500">
              📅{" "}
              {new Date(tournament.date).toLocaleDateString("en-US", {
                year: "numeric",
                month: "long",
                day: "numeric",
              })}
            </div>
          </Link>
        ))}
      </div>

      {tournaments.length === 0 && (
        <div className="text-center text-slate-400 py-12">
          No tournaments found. Make sure the backend is running and seeded with
          data.
        </div>
      )}

      {/* Teams Section */}
      <h1 className="text-3xl font-bold mb-8 text-white">Teams</h1>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        {teams.map((team) => (
          <Link
            key={team.id}
            href={`/team/${team.id}`}
            className="block bg-slate-800 rounded-lg p-5 border border-slate-700 hover:border-green-500 hover:bg-slate-750 transition-all duration-200 group"
          >
            <h2 className="text-lg font-semibold text-white group-hover:text-green-400 transition-colors mb-2">
              {team.name}
            </h2>
            <div className="text-sm text-slate-400">
              👥 {team.player_count} players
            </div>
          </Link>
        ))}
      </div>

      {teams.length === 0 && (
        <div className="text-center text-slate-400 py-12">
          No teams found. Make sure the backend is running and seeded with data.
        </div>
      )}
    </div>
  );
}
