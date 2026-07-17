from app.providers.gemini_provider import GeminiProvider


class SkillExtractorAgent:

    def __init__(self):
        self.ai = GeminiProvider()

    def extract(self, description: str):

        prompt = f"""
Extract ONLY the technical skills from this job description.

Return JSON.

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

        return self.ai.ask(prompt)
