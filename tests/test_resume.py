from io import BytesIO
from uuid import uuid4


def register_and_login(client):
    email = f"{uuid4().hex[:8]}@example.com"
    password = "Password123!"

    client.post(
        "/auth/register",
        json={
            "full_name": "Resume User",
            "email": email,
            "password": password,
        },
    )

    login = client.post(
        "/auth/login",
        data={
            "username": email,
            "password": password,
        },
    )

    token = login.json()["access_token"]

    return {"Authorization": f"Bearer {token}"}


def upload_resume(client, headers, mocker):
    mocker.patch(
        "app.services.resume_service.ResumeService.save_file",
        return_value=("resume.pdf", "uploads/resume.pdf"),
    )

    response = client.post(
        "/resume/upload",
        headers=headers,
        files={
            "file": (
                "resume.pdf",
                BytesIO(b"Dummy Resume"),
                "application/pdf",
            )
        },
    )

    assert response.status_code == 200

    return response.json()["resume_id"]


def test_upload_resume(client, mocker):
    headers = register_and_login(client)

    mocker.patch(
        "app.services.resume_service.ResumeService.save_file",
        return_value=("resume.pdf", "uploads/resume.pdf"),
    )

    response = client.post(
        "/resume/upload",
        headers=headers,
        files={
            "file": (
                "resume.pdf",
                BytesIO(b"Dummy Resume"),
                "application/pdf",
            )
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["success"] is True
    assert data["filename"] == "resume.pdf"


def test_get_resumes(client, mocker):
    headers = register_and_login(client)

    upload_resume(client, headers, mocker)

    response = client.get(
        "/resume/",
        headers=headers,
    )

    assert response.status_code == 200

    resumes = response.json()

    assert len(resumes) == 1


def test_get_resume(client, mocker):
    headers = register_and_login(client)

    resume_id = upload_resume(client, headers, mocker)

    response = client.get(
        f"/resume/{resume_id}",
        headers=headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["resume"]["id"] == resume_id


def test_analyze_resume(client, mocker):
    headers = register_and_login(client)

    resume_id = upload_resume(client, headers, mocker)

    mocker.patch(
        "app.services.resume_service.ResumeService.extract_resume",
        return_value="Python FastAPI SQL",
    )

    mocker.patch(
        "app.services.resume_service.ResumeService.analyze_with_cache",
        return_value={
            "ats_score": 95,
            "strengths": ["Python"],
            "missing_skills": [],
            "suggestions": [],
        },
    )

    response = client.post(
        f"/resume/{resume_id}/analyze",
        headers=headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["success"] is True
    assert data["analysis"]["ats_score"] == 95


def test_delete_resume(client, mocker):
    headers = register_and_login(client)

    resume_id = upload_resume(client, headers, mocker)

    mocker.patch("os.path.exists", return_value=True)
    mocker.patch("os.remove")

    response = client.delete(
        f"/resume/{resume_id}",
        headers=headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["success"] is True
    assert data["message"] == "Resume deleted successfully"
