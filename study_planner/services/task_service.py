from datetime import date

from sqlmodel import Session, select

from study_planner.domain.models import Task


class TaskService:
    def get_all_tasks(self, session: Session) -> list[Task]:
        statement = select(Task)
        return list(session.exec(statement))

    def get_urgent_tasks(self, session: Session) -> list[Task]:
        tasks = self.get_all_tasks(session)
        open_tasks = [task for task in tasks if not task.is_completed and task.deadline is not None]
        return sorted(open_tasks, key=lambda task: task.deadline)[:3]

    def get_upcoming_deadlines(self, session: Session) -> list[Task]:
        tasks = self.get_all_tasks(session)
        tasks_with_deadline = [task for task in tasks if not task.is_completed and task.deadline is not None]
        return sorted(tasks_with_deadline, key=lambda task: task.deadline)

    def get_task_progress(self, session: Session) -> dict[str, int]:
        tasks = self.get_all_tasks(session)
        total = len(tasks)
        completed = len([task for task in tasks if task.is_completed])
        open_tasks = total - completed
        return {
            "total": total,
            "completed": completed,
            "open": open_tasks,
        }

    def create_task(
        self,
        session: Session,
        title: str,
        deadline: date | None = None,
        notes: str = "",
        subject_id: int | None = None,
    ) -> Task:
        task = Task(
            title=title,
            deadline=deadline,
            notes=notes,
            subject_id=subject_id,
        )
        session.add(task)
        session.commit()
        session.refresh(task)
        return task

    def complete_task(self, session: Session, task_id: int) -> Task | None:
        task = session.get(Task, task_id)
        if task is None:
            return None

        task.is_completed = True
        session.add(task)
        session.commit()
        session.refresh(task)
        return task
