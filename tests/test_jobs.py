def test_search_jobs(client, mocker):
    expected_jobs = [
        {
            "title": "Python Developer",
            "company": "Google",
            "location": "Bangalore",
        },
        {
            "title": "Backend Engineer",
            "company": "Amazon",
            "location": "Chennai",
        },
    ]

    mock_search = mocker.patch(
        "app.agents.search_agent.JobSearchAgent.search",
        return_value=expected_jobs,
    )

    response = client.get("/jobs/search")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 2
    assert data[0]["title"] == "Python Developer"
    assert data[1]["company"] == "Amazon"

    mock_search.assert_called_once()
