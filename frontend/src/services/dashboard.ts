import api from "./api";

export async function getDashboardData() {
  const [jobs, match] = await Promise.all([
    api.get("/jobs/search"),
    api.get("/ai/match"),
  ]);

  return {
    jobs: jobs.data,
    match: match.data,
  };
}