from types import SimpleNamespace

from app.services.dashboard_service import DashboardService


def test_dashboard_no_analysis_no_matches(mocker):
    service = DashboardService(db=None)

    mocker.patch.object(
        service.analysis_repo,
        "get_by_resume",
        return_value=None,
    )

    mocker.patch.object(
        service.match_repo,
        "get_by_resume",
        return_value=[],
    )

    result = service.get_dashboard(1)

    assert result == {
        "resume_score": 0,
        "jobs_analyzed": 0,
        "average_match": 0,
        "highest_match": 0,
        "lowest_match": 0,
        "top_missing_skills": [],
    }


def test_dashboard_analysis_no_matches(mocker):
    service = DashboardService(db=None)

    analysis = SimpleNamespace(
        ats_score=87,
    )

    mocker.patch.object(
        service.analysis_repo,
        "get_by_resume",
        return_value=analysis,
    )

    mocker.patch.object(
        service.match_repo,
        "get_by_resume",
        return_value=[],
    )

    result = service.get_dashboard(1)

    assert result["resume_score"] == 87
    assert result["jobs_analyzed"] == 0
    assert result["average_match"] == 0


def test_dashboard_with_matches(mocker):
    service = DashboardService(db=None)

    analysis = SimpleNamespace(
        ats_score=92,
    )

    matches = [
        SimpleNamespace(
            match_score=80,
            missing_skills='["Docker","AWS"]',
        ),
        SimpleNamespace(
            match_score=90,
            missing_skills='["AWS","Kubernetes"]',
        ),
        SimpleNamespace(
            match_score=70,
            missing_skills='["Docker"]',
        ),
    ]

    mocker.patch.object(
        service.analysis_repo,
        "get_by_resume",
        return_value=analysis,
    )

    mocker.patch.object(
        service.match_repo,
        "get_by_resume",
        return_value=matches,
    )

    result = service.get_dashboard(1)

    assert result["resume_score"] == 92
    assert result["jobs_analyzed"] == 3
    assert result["average_match"] == 80
    assert result["highest_match"] == 90
    assert result["lowest_match"] == 70

    assert result["top_missing_skills"] == [
        "Docker",
        "AWS",
        "Kubernetes",
    ]


def test_dashboard_invalid_json_is_ignored(mocker):
    service = DashboardService(db=None)

    analysis = SimpleNamespace(
        ats_score=75,
    )

    matches = [
        SimpleNamespace(
            match_score=60,
            missing_skills="invalid json",
        ),
        SimpleNamespace(
            match_score=80,
            missing_skills='["Python"]',
        ),
    ]

    mocker.patch.object(
        service.analysis_repo,
        "get_by_resume",
        return_value=analysis,
    )

    mocker.patch.object(
        service.match_repo,
        "get_by_resume",
        return_value=matches,
    )

    result = service.get_dashboard(1)

    assert result["jobs_analyzed"] == 2
    assert result["average_match"] == 70
    assert result["highest_match"] == 80
    assert result["lowest_match"] == 60
    assert result["top_missing_skills"] == ["Python"]
