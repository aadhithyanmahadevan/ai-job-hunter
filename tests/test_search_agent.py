from types import SimpleNamespace

from app.agents.search_agent import JobSearchAgent


def create_job(
    salary_min=1000000,
    salary_max=2000000,
):
    return SimpleNamespace(
        title="Backend Engineer",
        company="Google",
        location="Bangalore",
        description="Python FastAPI",
        salary_min=salary_min,
        salary_max=salary_max,
        url="https://job1",
        source="Adzuna",
    )


def test_search_cache_hit(mocker):
    agent = JobSearchAgent(db=None)

    response = {"results": [{"id": 1}]}

    normalized = create_job()

    mocker.patch.object(
        agent.provider,
        "search_jobs",
        return_value=response,
    )

    mocker.patch(
        "app.agents.search_agent.normalize_adzuna",
        return_value=normalized,
    )

    mocker.patch(
        "app.agents.search_agent.JobSkillCache.get_hash",
        return_value="abc",
    )

    mocker.patch(
        "app.agents.search_agent.JobSkillCache.exists",
        return_value=True,
    )

    mocker.patch(
        "app.agents.search_agent.JobSkillCache.load",
        return_value={"skills": ["Python", "FastAPI"]},
    )

    mocker.patch.object(
        agent.repo,
        "exists",
        return_value=False,
    )

    mock_save = mocker.patch.object(
        agent.repo,
        "save",
    )

    mocker.patch.object(
        agent.repo,
        "count",
        return_value=1,
    )

    result = agent.search()

    assert result["new_jobs_added"] == 1
    assert result["total_jobs"] == 1
    assert result["jobs"][0]["skills"] == [
        "Python",
        "FastAPI",
    ]

    mock_save.assert_called_once()


def test_search_cache_miss(mocker):
    agent = JobSearchAgent(db=None)

    response = {"results": [{"id": 1}]}

    normalized = create_job()

    mocker.patch.object(
        agent.provider,
        "search_jobs",
        return_value=response,
    )

    mocker.patch(
        "app.agents.search_agent.normalize_adzuna",
        return_value=normalized,
    )

    mocker.patch(
        "app.agents.search_agent.JobSkillCache.get_hash",
        return_value="abc",
    )

    mocker.patch(
        "app.agents.search_agent.JobSkillCache.exists",
        return_value=False,
    )

    mock_ai = mocker.patch.object(
        agent.ai,
        "extract_job_skills",
        return_value={"skills": ["Docker"]},
    )

    mock_save_cache = mocker.patch(
        "app.agents.search_agent.JobSkillCache.save",
    )

    mocker.patch.object(
        agent.repo,
        "exists",
        return_value=True,
    )

    mocker.patch.object(
        agent.repo,
        "count",
        return_value=5,
    )

    result = agent.search()

    assert result["new_jobs_added"] == 0
    assert result["total_jobs"] == 5
    assert result["jobs"][0]["skills"] == ["Docker"]

    mock_ai.assert_called_once()
    mock_save_cache.assert_called_once()


def test_search_skill_extraction_failure(mocker):
    agent = JobSearchAgent(db=None)

    response = {"results": [{"id": 1}]}

    normalized = create_job()

    mocker.patch.object(
        agent.provider,
        "search_jobs",
        return_value=response,
    )

    mocker.patch(
        "app.agents.search_agent.normalize_adzuna",
        return_value=normalized,
    )

    mocker.patch(
        "app.agents.search_agent.JobSkillCache.get_hash",
        side_effect=Exception("Cache Error"),
    )

    mocker.patch.object(
        agent.repo,
        "exists",
        return_value=True,
    )

    mocker.patch.object(
        agent.repo,
        "count",
        return_value=2,
    )

    result = agent.search()

    assert result["jobs"][0]["skills"] == []


def test_salary_formats(mocker):
    agent = JobSearchAgent(db=None)

    jobs = [
        create_job(1000000, 2000000),
        create_job(1000000, None),
        create_job(None, 2000000),
        create_job(None, None),
    ]

    response = {"results": [{}, {}, {}, {}]}

    mocker.patch.object(
        agent.provider,
        "search_jobs",
        return_value=response,
    )

    mocker.patch(
        "app.agents.search_agent.normalize_adzuna",
        side_effect=jobs,
    )

    mocker.patch(
        "app.agents.search_agent.JobSkillCache.get_hash",
        return_value="abc",
    )

    mocker.patch(
        "app.agents.search_agent.JobSkillCache.exists",
        return_value=True,
    )

    mocker.patch(
        "app.agents.search_agent.JobSkillCache.load",
        return_value={"skills": []},
    )

    mocker.patch.object(
        agent.repo,
        "exists",
        return_value=True,
    )

    mocker.patch.object(
        agent.repo,
        "count",
        return_value=4,
    )

    result = agent.search()

    salaries = [j["salary"] for j in result["jobs"]]

    assert salaries[0] == "₹1,000,000 - ₹2,000,000"
    assert salaries[1] == "From ₹1,000,000"
    assert salaries[2] == "Up to ₹2,000,000"
    assert salaries[3] == "Not disclosed"
