import { useEffect, useState } from "react";
import { getMatch } from "../services/match";

export interface MatchResult {
  match_score: number;
  matched_skills: string[];
  missing_skills: string[];
  recommendation: string;
}

export default function useMatch(job: any) {
  const [result, setResult] = useState<MatchResult | null>(null);

  useEffect(() => {
    async function load() {
      try {
        const data = await getMatch(job);
        setResult(data);
      } catch (err) {
        console.error(err);
      }
    }

    load();
  }, [job]);

  return result;
}