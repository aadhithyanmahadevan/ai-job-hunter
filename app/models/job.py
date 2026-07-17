from datetime import datetime

from sqlalchemy import DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class Job(Base):
    __tablename__ = "jobs"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    title: Mapped[str] = mapped_column(String(255))
    company: Mapped[str] = mapped_column(String(255))
    location: Mapped[str] = mapped_column(String(255))

    description: Mapped[str] = mapped_column(Text)

    salary: Mapped[str] = mapped_column(
        String(100),
        default="Not specified",
    )

    url: Mapped[str] = mapped_column(
        String(500),
        unique=True,
    )

    source: Mapped[str] = mapped_column(
        String(50),
        default="manual",
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )