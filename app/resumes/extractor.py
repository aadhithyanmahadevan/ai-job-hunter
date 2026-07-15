import re

SKILLS = [
    "Python",
    "Java",
    "Selenium",
    "Playwright",
    "AWS",
    "Docker",
    "SQL",
    "FastAPI",
    "Spring Boot",
]


class ResumeExtractor:

    def extract_skills(self, text: str):

        found = []

        for skill in SKILLS:

            if re.search(skill, text, re.IGNORECASE):
                found.append(skill)

        return sorted(found)