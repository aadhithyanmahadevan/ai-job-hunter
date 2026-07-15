from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Job(Base):
    __tablename__ = "jobs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    title: Mapped[str] = mapped_column(String(255))
    company: Mapped[str] = mapped_column(String(255))
    location: Mapped[str] = mapped_column(String(255))

    description: Mapped[str] = mapped_column(Text)

    salary: Mapped[str] = mapped_column(String(100))

    url: Mapped[str] = mapped_column(String(500), unique=True)

    source: Mapped[str] = mapped_column(String(50))