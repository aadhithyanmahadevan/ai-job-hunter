import json
import time

from google import genai

from app.config.settings import settings


class GeminiProvider:

    def __init__(self):

        self.client = genai.Client(
            api_key=settings.GEMINI_API_KEY
        )

        # Try models in this order
        self.models = [
            "models/gemini-3.1-flash-lite",
            "models/gemini-3.5-flash",
            "models/gemini-2.0-flash",
        ]

    def _generate(self, prompt: str):

        last_error = None

        for model in self.models:

            print("=" * 60)
            print(f"Trying {model}")
            print("=" * 60)

            for attempt in range(3):

                try:

                    response = self.client.models.generate_content(
                        model=model,
                        contents=prompt,
                    )

                    print(f"SUCCESS: {model}")

                    return response.text

                except Exception as e:

                    print(
                        f"FAILED ({attempt + 1}/3): {model}"
                    )

                    print(e)

                    last_error = e

                    time.sleep(2 ** attempt)

        raise Exception(f"All Gemini models failed.\n\n{last_error}")

    def ask(self, prompt: str):

        response = self._generate(prompt)

        # Remove markdown code blocks if Gemini returns them
        response = response.replace("```json", "")
        response = response.replace("```", "")
        response = response.strip()

        return response

    def analyze_resume(self, resume_text: str):

        prompt = f"""
You are an expert technical recruiter.

Analyze this resume.

Return ONLY valid JSON.

Format:

{{
    "name":"",
    "title":"",
    "years_of_experience":"",
    "skills":[],
    "education":[],
    "certifications":[],
    "projects":[],
    "strengths":[],
    "missing_skills":[]
}}

Resume:

{resume_text}
"""

        result = self.ask(prompt)

        try:
            return json.loads(result)

        except Exception:
            return {
                "raw_response": result
            }

    def extract_job_skills(self, description: str):

        prompt = f"""
Extract ONLY technical skills from this job description.

Return ONLY JSON.

Example:

{{
    "skills":[
        "Java",
        "Spring Boot",
        "AWS",
        "Docker"
    ]
}}

Job Description:

{description}
"""

        result = self.ask(prompt)

        try:
            return json.loads(result)

        except Exception:
            return {
                "skills": []
            }