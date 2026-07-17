import json
from google import genai
from app.config.settings import settings

class GeminiProvider:
    def __init__(self):
        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)
        self.models = [
            "models/gemini-3.5-flash",
            "models/gemini-2.5-flash",
            "models/gemini-2.5-flash-lite",
            "models/gemini-3.1-flash-lite",
            "models/gemini-2.0-flash",
        ]
        self.last_working_index = 0

    def _generate(self, prompt: str):
        ordered = self.models[self.last_working_index:] + self.models[:self.last_working_index]
        last_error = None
        for model in ordered:
            try:
                response = self.client.models.generate_content(model=model, contents=prompt)
                self.last_working_index = self.models.index(model)
                return response.text
            except Exception as e:
                last_error = e
        raise RuntimeError(f"All Gemini models failed: {last_error}")

    def ask(self, prompt: str):
        return self._generate(prompt).replace("```json","").replace("```","").strip()

    def analyze_resume(self, resume_text: str):
        prompt = f"""
You are an expert recruiter.
Return ONLY JSON:
{{"name":"","title":"","years_of_experience":"","skills":[],"education":[],"certifications":[],"projects":[],"strengths":[],"missing_skills":[]}}

Resume:
{resume_text}
"""
        try:
            return json.loads(self.ask(prompt))
        except Exception:
            return {"raw_response": self.ask(prompt)}

    def extract_job_skills(self, description: str):
        prompt = f'Extract ONLY technical skills. Return JSON: {{"skills":[]}}\n\nJob:\n{description}'
        try:
            return json.loads(self.ask(prompt))
        except Exception:
            return {"skills":[]}

    def generate_interview_questions(self, job_description: str):
        prompt = f'Return ONLY JSON: {{"technical":[],"hr":[],"coding":[]}}\n\nJob:\n{job_description}'
        try:
            return json.loads(self.ask(prompt))
        except Exception:
            return {"technical":[],"hr":[],"coding":[]}

    def resume_improvements(self, resume_text: str, job_description: str):
        prompt = f'Return ONLY JSON: {{"strengths":[],"weaknesses":[],"suggestions":[]}}\n\nResume:\n{resume_text}\n\nJob:\n{job_description}'
        try:
            return json.loads(self.ask(prompt))
        except Exception:
            return {"strengths":[],"weaknesses":[],"suggestions":[]}

    def career_recommendation(self, resume: dict):
        prompt = f'Return ONLY JSON: {{"summary":"","next_steps":[]}}\n\nResume:\n{json.dumps(resume)}'
        try:
            return json.loads(self.ask(prompt))
        except Exception:
            return {"summary":"","next_steps":[]}

    def learning_roadmap(self, missing_skills: list):
        prompt = f'Return ONLY JSON: {{"weeks":[]}}\n\nMissing Skills:\n{json.dumps(missing_skills)}'
        try:
            return json.loads(self.ask(prompt))
        except Exception:
            return {"weeks":[]}
