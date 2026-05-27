from datetime import date, timedelta

from study_planner.services.subject_service import SubjectService
from study_planner.services.task_service import TaskService


def test_create_task_saves_task_with_subject(session):
    subject_service = SubjectService()
    task_service = TaskService()
    subject = subject_service.create_subject(session, "Programming", 6, "Semester 1", "")

    task = task_service.create_task(
        session,
        title="Finish Python assignment",
        deadline=date(2026, 5, 31),
        planned_date=date(2026, 5, 28),
        estimated_minutes=120,
        priority="high",
        notes="OOP part",
        subject_id=subject.id,
    )

    assert task.id is not None
    assert task.title == "Finish Python assignment"
    assert task.subject_id == subject.id
    assert task.is_completed is False


def test_complete_task_marks_task_as_completed(session):
    task_service = TaskService()
    task = task_service.create_task(session, "Read chapter")

    completed = task_service.complete_task(session, task.id)

    assert completed is not None
    assert completed.is_completed is True


def test_complete_task_returns_none_for_unknown_id(session):
    task_service = TaskService()

    completed = task_service.complete_task(session, 999)

    assert completed is None


def test_get_urgent_tasks_returns_three_open_tasks_sorted_by_deadline(session):
    task_service = TaskService()
    today = date.today()
    task_service.create_task(session, "Task in 5 days", deadline=today + timedelta(days=5))
    soon = task_service.create_task(session, "Task tomorrow", deadline=today + timedelta(days=1))
    medium = task_service.create_task(session, "Task in 3 days", deadline=today + timedelta(days=3))
    later = task_service.create_task(session, "Task in 10 days", deadline=today + timedelta(days=10))
    done = task_service.create_task(session, "Completed task", deadline=today)
    task_service.complete_task(session, done.id)

    urgent_tasks = task_service.get_urgent_tasks(session)

    assert [task.title for task in urgent_tasks] == [
        soon.title,
        medium.title,
        "Task in 5 days",
    ]
    assert later not in urgent_tasks
    assert done not in urgent_tasks


def test_get_task_progress_counts_total_completed_and_open(session):
    task_service = TaskService()
    done = task_service.create_task(session, "Done task")
    task_service.create_task(session, "Open task")
    task_service.complete_task(session, done.id)

    progress = task_service.get_task_progress(session)

    assert progress == {"total": 2, "completed": 1, "open": 1}


def test_get_priority_distribution_can_filter_by_semester(session):
    subject_service = SubjectService()
    task_service = TaskService()
    programming = subject_service.create_subject(session, "Programming", 6, "Semester 1", "")
    databases = subject_service.create_subject(session, "Databases", 5, "Semester 2", "")
    task_service.create_task(session, "Python assignment", priority="high", subject_id=programming.id)
    task_service.create_task(session, "Read docs", priority="medium", subject_id=programming.id)
    task_service.create_task(session, "SQL exercise", priority="low", subject_id=databases.id)

    distribution = task_service.get_priority_distribution(session, "Semester 1")

    assert distribution == {"high": 1, "medium": 1, "low": 0}


def test_get_tasks_per_subject_counts_tasks_for_each_subject(session):
    subject_service = SubjectService()
    task_service = TaskService()
    programming = subject_service.create_subject(session, "Programming", 6, "Semester 1", "")
    databases = subject_service.create_subject(session, "Databases", 5, "Semester 1", "")
    task_service.create_task(session, "Task 1", subject_id=programming.id)
    task_service.create_task(session, "Task 2", subject_id=programming.id)
    task_service.create_task(session, "Task 3", subject_id=databases.id)

    tasks_per_subject = task_service.get_tasks_per_subject(session, "Semester 1")

    assert tasks_per_subject == [
        {"subject": "Programming", "count": 2},
        {"subject": "Databases", "count": 1},
    ]
