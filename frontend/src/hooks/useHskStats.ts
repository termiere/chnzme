import { useEffect, useState } from "react";
import { getAddedWordsByHSK } from "../api/userWords";
import type { HskStatsDTO } from "../types/userWords";

export function useHskStats(hskLevel: number | null) {
  const [stats, setStats] = useState<HskStatsDTO | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (hskLevel === null) {
      setStats(null);
      setLoading(false);
      return;
    }

    let cancelled = false;
    setLoading(true);

    getAddedWordsByHSK(hskLevel)
      .then((data) => {
        if (!cancelled) setStats(data);
      })
      .catch((err) => {
        console.error(err);
        if (!cancelled) setStats(null);
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });

    return () => {
      cancelled = true;
    };
  }, [hskLevel]);

  return { stats, loading };
}
