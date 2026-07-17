import { useEffect, useState } from "react";
import { getJobs } from "../services/jobs";
import type { Job } from "../types";

export default function useJobs() {
  const [loading, setLoading] = useState(true);

  const [jobs, setJobs] = useState<Job[]>([]);

  useEffect(() => {
    async function loadJobs() {
      try {
        const data = await getJobs();

        // Backend returns { jobs: [...] }
        setJobs(data.jobs || []);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    }

    loadJobs();
  }, []);

  return {
    loading,
    jobs,
  };
}