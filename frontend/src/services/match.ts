import api from "./api";

export async function getMatch(job: any) {
  const response = await api.post(
    "/match/",
    job
  );

  return response.data;
}