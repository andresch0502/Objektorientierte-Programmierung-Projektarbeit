from study_planner.data_access.db import Database
from study_planner.domain.models import Subject
from study_planner.services.subject_service import SubjectService


database = Database()
subject_service = SubjectService()


def get_app_title() -> str:
    return "StudyPlanner"


def get_subjects() -> list[Subject]:
    with database.session_scope() as session:
        return subject_service.get_all_subjects(session)
