import api from "./api";

export async function analyzeResume() {
  const response = await api.post("/resume/analyze");

  return response.data;
}