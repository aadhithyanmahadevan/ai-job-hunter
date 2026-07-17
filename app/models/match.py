from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class Match(Base):
    __tablename__ = "matches"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    resume_id: Mapped[int] = mapped_column(
        ForeignKey("resumes.id"),
        nullable=False,
    )

    job_id: Mapped[int] = mapped_column(
        ForeignKey("jobs.id"),
        nullable=False,
    )

    match_score: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )

    matched_skills: Mapped[str] = mapped_column(
        Text,
        default="[]",
    )

    missing_skills: Mapped[str] = mapped_column(
        Text,
        default="[]",
    )

    recommendations: Mapped[str] = mapped_column(
        Text,
        default="",
    )

    raw_json: Mapped[str] = mapped_column(
        Text,
        default="{}",
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    resume = relationship(
        "Resume",
        lazy="joined",
    )

    job = relationship(
        "Job",
        lazy="joined",
    )
