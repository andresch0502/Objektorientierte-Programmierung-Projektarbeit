from study_planner.data_access.db import Database
from study_planner.domain.models import Subject, Task
from study_planner.services.subject_service import SubjectService
from study_planner.services.task_service import TaskService


database = Database()
subject_service = SubjectService()
task_service = TaskService()


def get_app_title() -> str:
    return "StudyPlanner"


def get_subjects() -> list[Subject]:
    with database.session_scope() as session:
        return subject_service.get_all_subjects(session)


def add_subject(name: str, description: str = "") -> Subject:
    with database.session_scope() as session:
        return subject_service.create_subject(session, name, description)


def get_tasks() -> list[Task]:
    with database.session_scope() as session:
        return task_service.get_all_tasks(session)


def add_task(title: str, description: str = "", subject_id: int | None = None) -> Task:
    with database.session_scope() as session:
        return task_service.create_task(session, title, description, subject_id)
