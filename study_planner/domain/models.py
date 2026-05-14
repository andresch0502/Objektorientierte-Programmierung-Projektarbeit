from datetime import date
from typing import Optional

from sqlmodel import Field, SQLModel


class Subject(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: str = ""


class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: str = ""
    deadline: Optional[date] = None
    is_completed: bool = False
    subject_id: Optional[int] = Field(default=None, foreign_key="subject.id")


class StudySession(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    session_date: date
    duration_minutes: int
    notes: str = ""
    subject_id: Optional[int] = Field(default=None, foreign_key="subject.id")
