from datetime import date

from sqlmodel import Session, select

from study_planner.domain.models import Subject, Task


class TaskService:
    def get_all_tasks(self, session: Session) -> list[Task]:
        statement = select(Task)
        return list(session.exec(statement))

    def _get_subject_ids_for_semester(
        self,
        session: Session,
        semester: str | None = None,
    ) -> set[int]:
        subjects = list(session.exec(select(Subject)))

        if semester and semester != "All semesters":
            subjects = [subject for subject in subjects if subject.semester == semester]

        return {subject.id for subject in subjects if subject.id is not None}

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

    def get_tasks_per_subject(
        self,
        session: Session,
        semester: str | None = None,
    ) -> list[dict[str, int | str]]:
        subjects = list(session.exec(select(Subject)))

        if semester and semester != "All semesters":
            subjects = [subject for subject in subjects if subject.semester == semester]

        tasks = self.get_all_tasks(session)

        result: list[dict[str, int | str]] = []
        for subject in subjects:
            if subject.id is None:
                continue

            count = len([task for task in tasks if task.subject_id == subject.id])
            result.append({
                "subject": subject.name,
                "count": count,
            })

        return result

    def get_priority_distribution(
        self,
        session: Session,
        semester: str | None = None,
    ) -> dict[str, int]:
        tasks = self.get_all_tasks(session)

        if semester and semester != "All semesters":
            subject_ids = self._get_subject_ids_for_semester(session, semester)
            tasks = [task for task in tasks if task.subject_id in subject_ids]

        return {
            "high": len([task for task in tasks if task.priority == "high"]),
            "medium": len([task for task in tasks if task.priority == "medium"]),
            "low": len([task for task in tasks if task.priority == "low"]),
        }

    def create_task(
        self,
        session: Session,
        title: str,
        deadline: date | None = None,
        planned_date: date | None = None,
        estimated_minutes: int = 0,
        priority: str = "medium",
        notes: str = "",
        subject_id: int | None = None,
    ) -> Task:
        task = Task(
            title=title,
            deadline=deadline,
            planned_date=planned_date,
            estimated_minutes=estimated_minutes,
            priority=priority,
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
