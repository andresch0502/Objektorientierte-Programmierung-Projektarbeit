from datetime import date

from sqlmodel import Session, select

from study_planner.domain.models import StudySession


class StudySessionService:
    def get_all_sessions(self, session: Session) -> list[StudySession]:
        statement = select(StudySession)
        return list(session.exec(statement))

    def get_study_statistics(self, session: Session) -> dict[str, int]:
        sessions = self.get_all_sessions(session)
        total_sessions = len(sessions)
        total_minutes = sum(study_session.duration_minutes for study_session in sessions)
        return {
            "total_sessions": total_sessions,
            "total_minutes": total_minutes,
        }

    def create_session(
        self,
        session: Session,
        session_date: date,
        duration_minutes: int,
        notes: str = "",
        subject_id: int | None = None,
    ) -> StudySession:
        study_session = StudySession(
            session_date=session_date,
            duration_minutes=duration_minutes,
            notes=notes,
            subject_id=subject_id,
        )
        session.add(study_session)
        session.commit()
        session.refresh(study_session)
        return study_session
