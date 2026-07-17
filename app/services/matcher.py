from typing import Dict, List


class AIMatcher:

    @staticmethod
    def calculate_match(
        resume: Dict,
        job_skills: List[str]
    ) -> Dict:

        resume_skills = {
            skill.lower().strip()
            for skill in resume.get("skills", [])
        }

        job_skills = {
            skill.lower().strip()
            for skill in job_skills
        }

        matched = sorted(
            resume_skills.intersection(job_skills)
        )

        missing = sorted(
            job_skills - resume_skills
        )

        if len(job_skills) == 0:
            score = 0
        else:
            score = int(
                (len(matched) / len(job_skills)) * 100
            )

        # AI Recommendation

        if score >= 90:
            recommendation = (
                "Excellent match. Apply immediately."
            )

        elif score >= 75:
            recommendation = (
                "Strong profile. Improve the missing skills for a higher chance."
            )

        elif score >= 50:
            recommendation = (
                "Good potential. Learn the missing skills before applying."
            )

        else:
            recommendation = (
                "Low match. Focus on building the required skills first."
            )

        return {
            "match_score": score,
            "matched_skills": matched,
            "missing_skills": missing,
            "recommendation": recommendation,
        }