import re

SKILLS = [
    "Java",
    "Python",
    "Spring Boot",
    "Spring",
    "SQL",
    "MySQL",
    "PostgreSQL",
    "Selenium",
    "Playwright",
    "Cypress",
    "JUnit",
    "TestNG",
    "REST",
    "REST API",
    "GraphQL",
    "Docker",
    "Kubernetes",
    "AWS",
    "Azure",
    "GCP",
    "Git",
    "GitHub",
    "Jenkins",
    "CI/CD",
    "FastAPI",
    "Kafka",
    "Redis",
    "MongoDB",
    "Linux",
    "Maven",
    "Gradle",
]


class ResumeExtractor:

    def extract_skills(self, text: str):

        found = []

        for skill in SKILLS:

            if re.search(skill, text, re.IGNORECASE):
                found.append(skill)

        return sorted(found)
