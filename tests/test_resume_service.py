import io
from fastapi import UploadFile

from app.services.resume_service import ResumeService


def test_save_file(tmp_path, mocker):
    mocker.patch(
        "app.services.resume_service.UPLOAD_DIR",
        tmp_path,
    )

    file = UploadFile(
        filename="resume.pdf",
        file=io.BytesIO(b"Resume Content"),
    )

    filename, filepath = ResumeService.save_file(file)

    assert filename == "resume.pdf"

    saved_file = tmp_path / "resume.pdf"

    assert saved_file.exists()
    assert filepath == str(saved_file)


def test_extract_resume(mocker):
    mock_extract = mocker.patch.object(
        ResumeService.parser,
        "extract_text",
        return_value="Extracted Resume Text",
    )

    result = ResumeService.extract_resume("resume.pdf")

    assert result == "Extracted Resume Text"

    mock_extract.assert_called_once_with("resume.pdf")


def test_analyze_resume(mocker):
    mock_ai = mocker.patch.object(
        ResumeService.ai,
        "analyze_resume",
        return_value={"score": 91},
    )

    result = ResumeService.analyze_resume("resume text")

    assert result == {"score": 91}

    mock_ai.assert_called_once_with("resume text")


def test_analyze_with_cache_hit(mocker):
    mocker.patch(
        "app.services.resume_service.ResumeCache.get_hash",
        return_value="abc123",
    )

    mocker.patch(
        "app.services.resume_service.ResumeCache.exists",
        return_value=True,
    )

    mocker.patch(
        "app.services.resume_service.ResumeCache.load",
        return_value={"score": 95},
    )

    mock_ai = mocker.patch.object(
        ResumeService.ai,
        "analyze_resume",
    )

    result = ResumeService.analyze_with_cache("resume text")

    assert result == {"score": 95}

    mock_ai.assert_not_called()


def test_analyze_with_cache_miss(mocker):
    mocker.patch(
        "app.services.resume_service.ResumeCache.get_hash",
        return_value="abc123",
    )

    mocker.patch(
        "app.services.resume_service.ResumeCache.exists",
        return_value=False,
    )

    mocker.patch(
        "app.services.resume_service.ResumeCache.save",
    )

    mock_ai = mocker.patch.object(
        ResumeService.ai,
        "analyze_resume",
        return_value={"score": 88},
    )

    result = ResumeService.analyze_with_cache("resume text")

    assert result == {"score": 88}

    mock_ai.assert_called_once_with("resume text")
