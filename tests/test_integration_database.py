from study_planner.data_access.db import Database
from study_planner.domain.models import Subject
from study_planner.services.subject_service import SubjectService


def test_database_session_scope_persists_subject_between_sessions(tmp_path):
    database_path = tmp_path / "study_planner_test.db"
    database = Database(f"sqlite:///{database_path}")
    database.init_schema()
    service = SubjectService()

    with database.session_scope() as session:
        service.create_subject(session, "Programming", 6, "Semester 1", "")

    with database.session_scope() as session:
        subjects = service.get_all_subjects(session)

    assert len(subjects) == 1
    assert subjects[0].name == "Programming"


def test_database_session_scope_rolls_back_when_exception_occurs(tmp_path):
    database_path = tmp_path / "rollback_test.db"
    database = Database(f"sqlite:///{database_path}")
    database.init_schema()

    try:
        with database.session_scope() as session:
            session.add(Subject(name="Should not be saved", ects=3))
            raise RuntimeError("force rollback")
    except RuntimeError:
        pass

    with database.session_scope() as session:
        subjects = session.query(Subject).all()

    assert subjects == []
