from sqlalchemy import Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Job(Base):
    __tablename__ = "jobs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    title: Mapped[str] = mapped_column(String)

    company: Mapped[str] = mapped_column(String)

    location: Mapped[str] = mapped_column(String)

    url: Mapped[str] = mapped_column(String, unique=True)