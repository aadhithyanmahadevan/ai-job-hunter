def test_generate_interview_questions(client, mocker):
    questions = [
        "Explain dependency injection.",
        "What is FastAPI?",
        "What is JWT authentication?",
    ]

    mock_generate = mocker.patch(
        "app.providers.gemini_provider.GeminiProvider.generate_interview_questions",
        return_value=questions,
    )

    response = client.post(
        "/interview/questions",
        json={"description": "Python FastAPI Developer"},
    )

    assert response.status_code == 200

    data = response.json()

    assert data["success"] is True
    assert data["data"] == questions

    mock_generate.assert_called_once_with("Python FastAPI Developer")


def test_generate_interview_questions_exception(client, mocker):
    mocker.patch(
        "app.providers.gemini_provider.GeminiProvider.generate_interview_questions",
        side_effect=Exception("Gemini API Error"),
    )

    response = client.post(
        "/interview/questions",
        json={"description": "Backend Developer"},
    )

    assert response.status_code == 500

    data = response.json()

    assert data["detail"] == "Gemini API Error"
