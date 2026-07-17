import api from "./api";

export async function getDashboardData() {
  const response = await api.get("/dashboard/summary");
  return response.data;
}