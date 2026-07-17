from types import SimpleNamespace

from app.services.match_service import MatchService


def test_analyze_returns_dict(mocker):
    service = MatchService(db=None)

    expected = {
        "score": 95,
        "strengths": ["Python"],
        "missing_skills": [],
        "recommendation": "Excellent",
    }

    mocker.patch.object(
        service.ai,
        "match_resume_to_job",
        return_value=expected,
    )

    result = service.analyze(
        "Resume",
        "Job Description",
    )

    assert result == expected


def test_analyze_returns_json_string(mocker):
    service = MatchService(db=None)

    json_result = """
    {
        "score":90,
        "strengths":["FastAPI"],
        "missing_skills":["Docker"],
        "recommendation":"Good"
    }
    """

    mocker.patch.object(
        service.ai,
        "match_resume_to_job",
        return_value=json_result,
    )

    result = service.analyze(
        "Resume",
        "Job",
    )

    assert result["score"] == 90
    assert result["strengths"] == ["FastAPI"]


def test_match_resume_resume_not_found(mocker):
    service = MatchService(db=None)

    mocker.patch.object(
        service.resume_repo,
        "get",
        return_value=None,
    )

    try:
        service.match_resume(1)
        assert False
    except Exception as e:
        assert str(e) == "Resume not found."


def test_match_resume_no_jobs(mocker):
    service = MatchService(db=None)

    resume = SimpleNamespace(
        id=1,
        extracted_text="Python",
    )

    mocker.patch.object(
        service.resume_repo,
        "get",
        return_value=resume,
    )

    mocker.patch.object(
        service.job_repo,
        "get_all",
        return_value=[],
    )

    try:
        service.match_resume(1)
        assert False
    except Exception as e:
        assert str(e) == "No jobs found."


def test_match_resume_success(mocker):
    service = MatchService(db=None)

    resume = SimpleNamespace(
        id=1,
        extracted_text="Python FastAPI",
    )

    jobs = [
        SimpleNamespace(
            id=1,
            title="Backend Developer",
            company="Google",
            location="Bangalore",
            salary="20 LPA",
            description="Python FastAPI",
        ),
        SimpleNamespace(
            id=2,
            title="Software Engineer",
            company="Amazon",
            location="Chennai",
            salary="18 LPA",
            description="Python",
        ),
    ]

    mocker.patch.object(
        service.resume_repo,
        "get",
        return_value=resume,
    )

    mocker.patch.object(
        service.job_repo,
        "get_all",
        return_value=jobs,
    )

    mocker.patch.object(
        service.match_repo,
        "delete_by_resume",
    )

    mocker.patch.object(
        service.match_repo,
        "create",
    )

    mocker.patch.object(
        service,
        "analyze",
        return_value={
            "score": 88,
            "strengths": ["Python"],
            "missing_skills": [],
            "recommendation": "Excellent",
        },
    )

    result = service.match_resume(1)

    assert result["resume_id"] == 1
    assert result["total_jobs"] == 2
    assert result["matched_jobs"] == 2

    assert len(result["top_matches"]) == 2

    assert result["top_matches"][0]["match_score"] == 88
