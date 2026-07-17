from fastapi import APIRouter

from app.services.state import state

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
)


@router.get("/summary")
def dashboard_summary():

    if state.resume is None:
        return {
            "resumeScore": 0,
            "skills": 0,
            "projects": 0,
            "certifications": 0,
            "strengths": [],
            "missingSkills": [],
            "resume": None,
        }

    resume = state.resume

    score = 0

    score += min(len(resume["skills"]) * 2, 40)
    score += min(len(resume["projects"]) * 5, 20)
    score += min(len(resume["certifications"]) * 5, 15)
    score += min(len(resume["education"]) * 10, 10)
    score -= min(len(resume["missing_skills"]) * 2, 15)

    score = max(0, min(score, 100))

    return {

        "resumeScore": score,

        "skills": len(resume["skills"]),

        "projects": len(resume["projects"]),

        "certifications": len(resume["certifications"]),

        "strengths": resume["strengths"],

        "missingSkills": resume["missing_skills"],

        "resume": resume,

    }