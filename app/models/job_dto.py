from dataclasses import dataclass


@dataclass
class JobDTO:
    title: str
    company: str
    location: str
    description: str
    salary_min: float | None
    salary_max: float | None
    url: str
    source: str
