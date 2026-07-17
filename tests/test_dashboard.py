from types import SimpleNamespace


def test_dashboard_summary(client, auth_user, mocker):
    resume = SimpleNamespace(
        id=1,
        user_id=auth_user.id,
    )

    dashboard = {
        "resume_score": 91,
        "jobs_analyzed": 15,
        "average_match": 82,
        "highest_match": 96,
        "lowest_match": 63,
        "top_missing_skills": [
            "Docker",
            "AWS",
        ],
    }

    mocker.patch(
        "app.database.resume_repository.ResumeRepository.get",
        return_value=resume,
    )

    mocker.patch(
        "app.services.dashboard_service.DashboardService.get_dashboard",
        return_value=dashboard,
    )

    response = client.get("/dashboard/1")

    assert response.status_code == 200

    data = response.json()

    assert data["resume_score"] == 91
    assert data["jobs_analyzed"] == 15
    assert data["highest_match"] == 96


def test_dashboard_resume_not_found(client, auth_user, mocker):
    mocker.patch(
        "app.database.resume_repository.ResumeRepository.get",
        return_value=None,
    )

    response = client.get("/dashboard/1")

    assert response.status_code == 404
    assert response.json()["detail"] == "Resume not found"


def test_dashboard_unauthorized(client, auth_user, mocker):
    resume = SimpleNamespace(
        id=1,
        user_id=999,
    )

    mocker.patch(
        "app.database.resume_repository.ResumeRepository.get",
        return_value=resume,
    )

    response = client.get("/dashboard/1")

    assert response.status_code == 403
    assert response.json()["detail"] == "Unauthorized"
