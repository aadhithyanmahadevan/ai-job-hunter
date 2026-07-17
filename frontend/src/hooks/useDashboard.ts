import { useEffect, useState } from "react";
import { getDashboardData } from "../services/dashboard";
import type { DashboardSummary } from "../types";

export default function useDashboard() {
  const [loading, setLoading] = useState(true);

  const [dashboard, setDashboard] =
    useState<DashboardSummary | null>(null);

  useEffect(() => {
    async function load() {
      try {
        const data = await getDashboardData();

        setDashboard(data);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    }

    load();
  }, []);

  return {
    loading,

    dashboard,

    resume: dashboard?.resume,

    resumeScore: dashboard?.resumeScore ?? 0,

    skillsCount: dashboard?.skills ?? 0,

    projectsCount: dashboard?.projects ?? 0,

    certificationsCount:
      dashboard?.certifications ?? 0,

    strengths:
      dashboard?.strengths ?? [],

    missingSkills:
      dashboard?.missingSkills ?? [],
  };
}