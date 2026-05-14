from datetime import date

from sqlmodel import Session, select

from study_planner.domain.models import Task


class TaskService:
    def get_all_tasks(self, session: Session) -> list[Task]:
        statement = select(Task)
        return list(session.exec(statement))

    def create_task(
        self,
        session: Session,
        title: str,
        description: str = "",
        deadline: date | None = None,
        subject_id: int | None = None,
    ) -> Task:
        task = Task(
            title=title,
            description=description,
            deadline=deadline,
            subject_id=subject_id,
        )
        session.add(task)
        session.commit()
        session.refresh(task)
        return task
