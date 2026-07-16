from typing import List


def calculate_skill_match(
    resume_skills: List[str],
    job_skills: List[str],
):
    resume = {skill.lower() for skill in resume_skills}
    job = {skill.lower() for skill in job_skills}

    matched = sorted(resume & job)
    missing = sorted(job - resume)

    if not job:
        score = 0
    else:
        score = round((len(matched) / len(job)) * 100, 2)

    return score, matched, missing