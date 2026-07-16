from dataclasses import dataclass


@dataclass
class JobMatch:
    title: str
    company: str
    location: str
    url: str

    match_score: float

    matched_skills: list[str]
    missing_skills: list[str]