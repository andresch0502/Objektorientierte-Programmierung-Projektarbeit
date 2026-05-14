from datetime import date
from typing import Optional

from sqlmodel import Field, SQLModel


class Subject(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    ects: int = 0


class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    deadline: Optional[date] = None
    planned_date: Optional[date] = None
    estimated_minutes: int = 0
    priority: str = "medium"
    is_completed: bool = False
    notes: str = ""
    subject_id: Optional[int] = Field(default=None, foreign_key="subject.id")
