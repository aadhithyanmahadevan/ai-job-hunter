from dataclasses import dataclass
from typing import Optional


@dataclass
class Job:
    title: str
    company: str
    location: str
    description: str

    salary_min: Optional[float]
    salary_max: Optional[float]

    url: str
    source: str