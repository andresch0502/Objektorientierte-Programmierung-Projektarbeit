from sqlmodel import Session, select

from study_planner.domain.models import Subject


class SubjectService:
    def get_all_subjects(self, session: Session) -> list[Subject]:
        statement = select(Subject)
        return list(session.exec(statement))

    def create_subject(self, session: Session, name: str, ects: int = 0) -> Subject:
        subject = Subject(name=name, ects=ects)
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
