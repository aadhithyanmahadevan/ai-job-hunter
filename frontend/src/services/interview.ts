import api from "./api";

export async function getInterviewQuestions(description: string) {
  const response = await api.post("/interview/questions", {
    description,
  });

  return response.data;
}