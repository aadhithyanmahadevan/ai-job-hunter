from app.providers.gemini_provider import GeminiProvider


class ResumeMatchAgent:

    def __init__(self):
        self.ai = GeminiProvider()

    def match(self, resume, job):

        prompt = f"""
You are an expert technical recruiter.

Compare this resume with the job.

Resume

{resume}

Job

{job}

Return ONLY JSON.

{{
    "match_score":95,
    "matched_skills":[],
    "missing_skills":[],
    "strengths":[],
    "recommendations":[]
}}
"""

        return self.ai.ask(prompt)