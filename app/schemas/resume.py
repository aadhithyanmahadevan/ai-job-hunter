from datetime import datetime

from pydantic import BaseModel


class ResumeResponse(BaseModel):
    id: int
    filename: str
    status: str
    uploaded_at: datetime

    model_config = {
        "from_attributes": True
    }


class ResumeDetail(BaseModel):
    id: int
    filename: str
    extracted_text: str
    status: str
    uploaded_at: datetime

    model_config = {
        "from_attributes": True
    }


class ResumeUploadResponse(BaseModel):
    success: bool
    resume_id: int
    filename: str
    message: str


class ResumeDeleteResponse(BaseModel):
    success: bool
    message: str