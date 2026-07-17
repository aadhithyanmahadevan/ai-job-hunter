from types import SimpleNamespace


def test_match_resume_to_job(client, auth_user, mocker):
    resume = SimpleNamespace(
        id=1,
        user_id=auth_user.id,
        extracted_text="Python FastAPI SQL",
    )

    job = SimpleNamespace(
        id=1,
        description="Python FastAPI Developer",
    )

    mocker.patch(
        "app.database.resume_repository.ResumeRepository.get",
        return_value=resume,
    )

    mocker.patch(
        "app.database.job_repository.JobRepository.get",
        return_value=job,
    )

    mocker.patch(
        "app.services.match_service.MatchService.analyze",
        return_value={
            "score": 92,
            "strengths": ["Python", "FastAPI"],
            "missing_skills": [],
            "recommendation": "Excellent Match",
        },
    )

    mock_create = mocker.patch("app.database.match_repository.MatchRepository.create")

    response = client.post(
        "/match/",
        params={
            "resume_id": 1,
            "job_id": 1,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["score"] == 92
    assert data["recommendation"] == "Excellent Match"

    mock_create.assert_called_once()


def test_match_resume_not_found(client, auth_user, mocker):
    mocker.patch(
        "app.database.resume_repository.ResumeRepository.get",
        return_value=None,
    )

    response = client.post(
        "/match/",
        params={
            "resume_id": 1,
            "job_id": 1,
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Resume not found"


def test_match_resume_endpoint(client, auth_user, mocker):
    resume = SimpleNamespace(
        id=1,
        user_id=auth_user.id,
    )

    mocker.patch(
        "app.database.resume_repository.ResumeRepository.get",
        return_value=resume,
    )

    mocker.patch(
        "app.services.match_service.MatchService.match_resume",
        return_value=[
            {
                "job_title": "Backend Developer",
                "score": 88,
            }
        ],
    )

    response = client.post("/match/resume/1")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["score"] == 88


def test_get_match_history(client, auth_user, mocker):
    resume = SimpleNamespace(
        id=1,
        user_id=auth_user.id,
    )

    history = [
        {
            "job": "Python Developer",
            "score": 90,
        }
    ]

    mocker.patch(
        "app.database.resume_repository.ResumeRepository.get",
        return_value=resume,
    )

    mocker.patch(
        "app.database.match_repository.MatchRepository.get_by_resume",
        return_value=history,
    )

    response = client.get("/match/1")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["score"] == 90
