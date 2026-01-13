"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import Link from "next/link";
import { getTournament, TournamentDetail, Match } from "@/lib/api";

interface RoundMatches {
  [key: string]: Match[];
}

const ROUND_ORDER = ['quarterfinals', 'semifinals', 'finals'];

export default function TournamentPage() {
  const params = useParams();
  const [tournament, setTournament] = useState<TournamentDetail | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (params.id) {
      getTournament(Number(params.id))
        .then(setTournament)
        .catch((err) => setError(err.message))
        .finally(() => setLoading(false));
    }
  }, [params.id]);

  if (loading) {
    return (
      <div className="flex justify-center items-center min-h-[50vh]">
        <div className="text-xl text-slate-400">Loading tournament...</div>
      </div>
    );
  }

  if (error || !tournament) {
    return (
      <div className="flex flex-col justify-center items-center min-h-[50vh] gap-4">
        <div className="text-xl text-red-400">Error: {error || 'Tournament not found'}</div>
        <Link href="/" className="text-blue-400 hover:text-blue-300">
          ← Back to tournaments
        </Link>
      </div>
    );
  }

  // Group matches by round
  const matchesByRound: RoundMatches = {};
  tournament.matches.forEach((match) => {
    if (!matchesByRound[match.round_name]) {
      matchesByRound[match.round_name] = [];
    }
    matchesByRound[match.round_name].push(match);
  });

  // Sort matches within each round
  Object.keys(matchesByRound).forEach((round) => {
    matchesByRound[round].sort((a, b) => a.match_number - b.match_number);
  });

  // Get rounds in order
  const rounds = ROUND_ORDER.filter((round) => matchesByRound[round]);

  return (
    <div>
      <Link href="/" className="text-blue-400 hover:text-blue-300 mb-6 inline-block">
        ← Back to tournaments
      </Link>

      <div className="mb-8">
        <div className="flex items-center gap-4 mb-2">
          <h1 className="text-3xl font-bold text-white">{tournament.name}</h1>
          <span className="text-sm bg-blue-600 text-white px-2 py-1 rounded">
            {tournament.tournament_type === 'single_elimination' ? 'Single Elimination' : tournament.tournament_type}
          </span>
        </div>
        <p className="text-slate-400 mb-2">{tournament.description}</p>
        <div className="text-sm text-slate-500">
          📅 {new Date(tournament.date).toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'long',
            day: 'numeric'
          })}
        </div>
      </div>

      {/* Bracket Display */}
      <div className="bg-slate-800 rounded-lg p-6 border border-slate-700">
        <h2 className="text-2xl font-bold text-white mb-6">Tournament Bracket</h2>

        <div className="flex gap-8 overflow-x-auto pb-4">
          {rounds.map((roundName) => (
            <div key={roundName} className="flex-shrink-0 min-w-[280px]">
              <h3 className="text-lg font-semibold text-blue-400 mb-4 text-center capitalize">
                {roundName.replace('_', ' ')}
              </h3>
              <div className="flex flex-col gap-4 justify-around h-full">
                {matchesByRound[roundName].map((match) => (
                  <MatchCard key={match.id} match={match} />
                ))}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Champion Display */}
      {matchesByRound['finals'] && matchesByRound['finals'][0]?.winner && (
        <div className="mt-8 bg-gradient-to-r from-yellow-600 to-yellow-500 rounded-lg p-6 text-center">
          <div className="text-lg text-yellow-100 mb-2">🏆 Champion 🏆</div>
          <div className="text-3xl font-bold text-white">
            {matchesByRound['finals'][0].winner.name}
          </div>
        </div>
      )}
    </div>
  );
}

function MatchCard({ match }: { match: Match }) {
  const isTeam1Winner = match.winner?.id === match.team1.id;
  const isTeam2Winner = match.winner?.id === match.team2.id;

  return (
    <div className="bg-slate-700 rounded-lg overflow-hidden border border-slate-600">
      <div
        className={`p-3 border-b border-slate-600 flex justify-between items-center ${
          isTeam1Winner ? 'bg-green-900/30' : ''
        }`}
      >
        <span className={`font-medium ${isTeam1Winner ? 'text-green-400' : 'text-slate-300'}`}>
          {match.team1.name}
        </span>
        {isTeam1Winner && <span className="text-green-400 text-sm">✓ W</span>}
        {isTeam2Winner && <span className="text-red-400 text-sm">L</span>}
      </div>
      <div
        className={`p-3 flex justify-between items-center ${
          isTeam2Winner ? 'bg-green-900/30' : ''
        }`}
      >
        <span className={`font-medium ${isTeam2Winner ? 'text-green-400' : 'text-slate-300'}`}>
          {match.team2.name}
        </span>
        {isTeam2Winner && <span className="text-green-400 text-sm">✓ W</span>}
        {isTeam1Winner && <span className="text-red-400 text-sm">L</span>}
      </div>
    </div>
  );
}
