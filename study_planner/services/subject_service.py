from sqlmodel import Session, select

from study_planner.domain.models import Subject


class SubjectService:
    def get_all_subjects(self, session: Session) -> list[Subject]:
        statement = select(Subject)
        return list(session.exec(statement))

    def create_subject(
        self,
        session: Session,
        name: str,
        ects: int = 0,
        semester: str = "Semester 1",
        moodle_link: str = "",
    ) -> Subject:
        subject = Subject(
            name=name,
            ects=ects,
            semester=semester,
            moodle_link=moodle_link,
            is_completed=False,
        )
        session.add(subject)
        session.commit()
        session.refresh(subject)
        return subject

    def update_subject(
        self,
        session: Session,
        subject_id: int,
        name: str,
        ects: int,
        semester: str,
        moodle_link: str,
        is_completed: bool,
    ) -> Subject | None:
        subject = session.get(Subject, subject_id)
        if subject is None:
            return None

        subject.name = name
        subject.ects = ects
        subject.semester = semester
        subject.moodle_link = moodle_link
        subject.is_completed = is_completed

        session.add(subject)
        session.commit()
        session.refresh(subject)
        return subject

    def delete_subject(self, session: Session, subject_id: int) -> bool:
        subject = session.get(Subject, subject_id)
        if subject is None:
            return False

        session.delete(subject)
        session.commit()
        return True

    def get_credit_summary(self, session: Session, semester: str | None = None) -> dict[str, int]:
        subjects = self.get_all_subjects(session)

        if semester and semester != "All semesters":
            subjects = [subject for subject in subjects if subject.semester == semester]

        planned = sum(subject.ects for subject in subjects)
        completed = sum(subject.ects for subject in subjects if subject.is_completed)
        open_credits = planned - completed

        return {
            "planned": planned,
            "completed": completed,
            "open": open_credits,
        }
