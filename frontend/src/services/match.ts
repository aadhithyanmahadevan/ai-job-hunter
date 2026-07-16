import api from "./api";

export async function getMatch() {
  const response = await api.get("/ai/match");

  return response.data;
}