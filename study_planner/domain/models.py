from datetime import date

from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(index=True)
    password_hash: str


class Subject(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    ects: int = 0
    semester: str = "Semester 1"
    moodle_link: str = ""
    is_completed: bool = False


class Task(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    deadline: date | None = None
    planned_date: date | None = None
    estimated_minutes: int = 0
    priority: str = "medium"
    is_completed: bool = False
    notes: str = ""
    subject_id: int | None = Field(default=None, foreign_key="subject.id")
