from sqlmodel import Session, select

from study_planner.domain.models import Subject


class SubjectService:
    def get_all_subjects(self, session: Session) -> list[Subject]:
        statement = select(Subject)
        return list(session.exec(statement))

    def create_subject(self, session: Session, name: str, description: str = "") -> Subject:
        subject = Subject(name=name, description=description)
        session.add(subject)
        session.commit()
        session.refresh(subject)
        return subject
