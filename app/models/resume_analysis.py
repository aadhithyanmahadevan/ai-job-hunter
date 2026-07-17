from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class ResumeAnalysis(Base):
    __tablename__ = "resume_analysis"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    resume_id: Mapped[int] = mapped_column(
        ForeignKey("resumes.id"),
        nullable=False,
    )

    ats_score: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )

    strengths: Mapped[str] = mapped_column(
        Text,
        default="[]",
    )

    missing_skills: Mapped[str] = mapped_column(
        Text,
        default="[]",
    )

    suggestions: Mapped[str] = mapped_column(
        Text,
        default="[]",
    )

    raw_json: Mapped[str] = mapped_column(
        Text,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    resume = relationship(
        "Resume",
        back_populates="analyses",
    )
