import api from "./api";

export async function getJobs() {
  const response = await api.get("/jobs/search");

  return response.data;
}