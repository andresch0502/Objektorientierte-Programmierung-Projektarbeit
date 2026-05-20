from datetime import date, timedelta

from sqlmodel import Session, select

from study_planner.domain.models import Subject, Task


def seed_demo_data(session: Session) -> None:
    existing_subject = session.exec(select(Subject)).first()
    if existing_subject is not None:
        return

    subjects = [
        Subject(name="Mathematics", ects=6, semester="Semester 1", moodle_link="https://moodle.example.com/math", is_completed=False),
        Subject(name="Programming", ects=6, semester="Semester 1", moodle_link="https://moodle.example.com/programming", is_completed=True),
        Subject(name="Databases", ects=5, semester="Semester 2", moodle_link="https://moodle.example.com/databases", is_completed=False),
        Subject(name="Statistics", ects=5, semester="Semester 2", moodle_link="https://moodle.example.com/statistics", is_completed=False),
        Subject(name="Software Engineering", ects=6, semester="Semester 3", moodle_link="https://moodle.example.com/se", is_completed=False),
        Subject(name="Web Development", ects=5, semester="Semester 3", moodle_link="https://moodle.example.com/webdev", is_completed=False),
        Subject(name="Computer Networks", ects=5, semester="Semester 4", moodle_link="https://moodle.example.com/networks", is_completed=False),
        Subject(name="Operating Systems", ects=6, semester="Semester 4", moodle_link="https://moodle.example.com/os", is_completed=False),
        Subject(name="Project Management", ects=4, semester="Semester 5", moodle_link="https://moodle.example.com/pm", is_completed=True),
        Subject(name="Machine Learning", ects=6, semester="Semester 5", moodle_link="https://moodle.example.com/ml", is_completed=False),
        Subject(name="Cyber Security", ects=5, semester="Semester 6", moodle_link="https://moodle.example.com/security", is_completed=False),
        Subject(name="Cloud Computing", ects=5, semester="Semester 6", moodle_link="https://moodle.example.com/cloud", is_completed=False),
    ]

    for subject in subjects:
        session.add(subject)

    session.commit()

    saved_subjects = list(session.exec(select(Subject)))
    subject_map = {subject.name: subject.id for subject in saved_subjects if subject.id is not None}

    today = date.today()

    tasks = [
        Task(
            title="Prepare algebra exercises",
            deadline=today + timedelta(days=2),
            planned_date=today + timedelta(days=1),
            estimated_minutes=90,
            priority="high",
            notes="Focus on linear equations",
            subject_id=subject_map.get("Mathematics"),
        ),
        Task(
            title="Finish Python assignment",
            deadline=today + timedelta(days=3),
            planned_date=today + timedelta(days=2),
            estimated_minutes=120,
            priority="high",
            notes="Complete object-oriented part",
            subject_id=subject_map.get("Programming"),
        ),
        Task(
            title="Review SQL joins",
            deadline=today + timedelta(days=5),
            planned_date=today + timedelta(days=4),
            estimated_minutes=60,
            priority="medium",
            notes="Practice inner and outer joins",
            subject_id=subject_map.get("Databases"),
        ),
        Task(
            title="Work on probability sheet",
            deadline=today + timedelta(days=6),
            planned_date=today + timedelta(days=5),
            estimated_minutes=75,
            priority="medium",
            notes="Focus on distributions",
            subject_id=subject_map.get("Statistics"),
        ),
        Task(
            title="Read UML chapter",
            deadline=today + timedelta(days=7),
            planned_date=today + timedelta(days=6),
            estimated_minutes=45,
            priority="low",
            notes="Take notes for class",
            subject_id=subject_map.get("Software Engineering"),
        ),
        Task(
            title="Design HTML mockup",
            deadline=today + timedelta(days=4),
            planned_date=today + timedelta(days=3),
            estimated_minutes=80,
            priority="medium",
            notes="Landing page only",
            subject_id=subject_map.get("Web Development"),
        ),
        Task(
            title="Configure subnetting exercise",
            deadline=today + timedelta(days=8),
            planned_date=today + timedelta(days=7),
            estimated_minutes=50,
            priority="medium",
            notes="CIDR practice",
            subject_id=subject_map.get("Computer Networks"),
        ),
        Task(
            title="Summarize process scheduling",
            deadline=today + timedelta(days=9),
            planned_date=today + timedelta(days=8),
            estimated_minutes=70,
            priority="low",
            notes="Short summary for exam prep",
            subject_id=subject_map.get("Operating Systems"),
        ),
        Task(
            title="Prepare team milestone report",
            deadline=today + timedelta(days=4),
            planned_date=today + timedelta(days=2),
            estimated_minutes=55,
            priority="high",
            notes="Include budget and timeline",
            subject_id=subject_map.get("Project Management"),
        ),
        Task(
            title="Train classification model",
            deadline=today + timedelta(days=10),
            planned_date=today + timedelta(days=9),
            estimated_minutes=110,
            priority="high",
            notes="Try second dataset too",
            subject_id=subject_map.get("Machine Learning"),
        ),
        Task(
            title="Review encryption basics",
            deadline=today + timedelta(days=11),
            planned_date=today + timedelta(days=10),
            estimated_minutes=65,
            priority="medium",
            notes="Symmetric vs asymmetric",
            subject_id=subject_map.get("Cyber Security"),
        ),
        Task(
            title="Compare cloud service models",
            deadline=today + timedelta(days=12),
            planned_date=today + timedelta(days=11),
            estimated_minutes=40,
            priority="low",
            notes="IaaS, PaaS, SaaS",
            subject_id=subject_map.get("Cloud Computing"),
        ),
    ]

    for task in tasks:
        session.add(task)

    session.commit()
