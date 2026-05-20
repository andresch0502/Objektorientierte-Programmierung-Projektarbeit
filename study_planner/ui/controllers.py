from datetime import date

from study_planner.data_access.db import Database
from study_planner.domain.models import Subject, Task
from study_planner.services.export_service import ExportService
from study_planner.services.subject_service import SubjectService
from study_planner.services.task_service import TaskService


database = Database()
subject_service = SubjectService()
task_service = TaskService()
export_service = ExportService()


def get_app_title() -> str:
    return "StudyPlanner"


def get_subjects() -> list[Subject]:
    with database.session_scope() as session:
        return subject_service.get_all_subjects(session)


def add_subject(
    name: str,
    ects: int = 0,
    semester: str = "Semester 1",
    moodle_link: str = "",
) -> Subject:
    with database.session_scope() as session:
        return subject_service.create_subject(session, name, ects, semester, moodle_link)


def edit_subject(
    subject_id: int,
    name: str,
    ects: int,
    semester: str,
    moodle_link: str,
    is_completed: bool,
) -> Subject | None:
    with database.session_scope() as session:
        return subject_service.update_subject(
            session,
            subject_id,
            name,
            ects,
            semester,
            moodle_link,
            is_completed,
        )


def remove_subject(subject_id: int) -> bool:
    with database.session_scope() as session:
        return subject_service.delete_subject(session, subject_id)


def get_credit_summary(semester: str | None = None) -> dict[str, int]:
    with database.session_scope() as session:
        return subject_service.get_credit_summary(session, semester)


def get_semester_statistics() -> list[dict[str, int | str]]:
    with database.session_scope() as session:
        return subject_service.get_semester_statistics(session)


def get_completed_subjects(semester: str | None = None) -> list[Subject]:
    with database.session_scope() as session:
        return subject_service.get_completed_subjects(session, semester)


def get_tasks() -> list[Task]:
    with database.session_scope() as session:
        return task_service.get_all_tasks(session)


def get_tasks_per_subject(semester: str | None = None) -> list[dict[str, int | str]]:
    with database.session_scope() as session:
        return task_service.get_tasks_per_subject(session, semester)


def get_priority_distribution(semester: str | None = None) -> dict[str, int]:
    with database.session_scope() as session:
        return task_service.get_priority_distribution(session, semester)


def export_subjects_csv() -> str:
    subjects = get_subjects()
    return export_service.export_subjects_to_csv(subjects, "exports/subjects_export.csv")


def export_tasks_csv() -> str:
    tasks = get_tasks()
    return export_service.export_tasks_to_csv(tasks, "exports/tasks_export.csv")


def add_task(
    title: str,
    deadline: date | None = None,
    planned_date: date | None = None,
    estimated_minutes: int = 0,
    priority: str = "medium",
    notes: str = "",
    subject_id: int | None = None,
) -> Task:
    with database.session_scope() as session:
        return task_service.create_task(
            session,
            title,
            deadline,
            planned_date,
            estimated_minutes,
            priority,
            notes,
            subject_id,
        )


def complete_task(task_id: int) -> Task | None:
    with database.session_scope() as session:
        return task_service.complete_task(session, task_id)
