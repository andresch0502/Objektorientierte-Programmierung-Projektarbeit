from datetime import date, timedelta
import re
import unicodedata

from sqlmodel import Session, select

from study_planner.domain.models import Subject, Task


def _slugify(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value)
    ascii_value = normalized.encode("ascii", "ignore").decode("ascii")
    ascii_value = ascii_value.lower()
    ascii_value = re.sub(r"[^a-z0-9]+", "-", ascii_value).strip("-")
    return ascii_value or "module"


def _moodle_link(module_name: str) -> str:
    return f"https://moodle.example.com/{_slugify(module_name)}"


def seed_demo_data(session: Session) -> None:
    existing_subject = session.exec(select(Subject)).first()
    if existing_subject is not None:
        return

    subjects = [
        # Semester 1
        Subject(
            name="Kritisches Denken und wissenschaftliches Schreiben",
            ects=6,
            semester="Semester 1",
            moodle_link=_moodle_link("Kritisches Denken und wissenschaftliches Schreiben"),
            is_completed=True,
        ),
        Subject(
            name="Angewandte Mathematik 1",
            ects=3,
            semester="Semester 1",
            moodle_link=_moodle_link("Angewandte Mathematik 1"),
            is_completed=True,
        ),
        Subject(
            name="Statistik 1",
            ects=3,
            semester="Semester 1",
            moodle_link=_moodle_link("Statistik 1"),
            is_completed=True,
        ),
        Subject(
            name="Principles of Management",
            ects=6,
            semester="Semester 1",
            moodle_link=_moodle_link("Principles of Management"),
            is_completed=True,
        ),
        Subject(
            name="Digital Business",
            ects=6,
            semester="Semester 1",
            moodle_link=_moodle_link("Digital Business"),
            is_completed=True,
        ),
        Subject(
            name="Grundlagen Programmierung",
            ects=6,
            semester="Semester 1",
            moodle_link=_moodle_link("Grundlagen Programmierung"),
            is_completed=True,
        ),

        # Semester 2
        Subject(
            name="Communication Essentials",
            ects=3,
            semester="Semester 2",
            moodle_link=_moodle_link("Communication Essentials"),
            is_completed=False,
        ),
        Subject(
            name="Angewandte Mathematik 2",
            ects=3,
            semester="Semester 2",
            moodle_link=_moodle_link("Angewandte Mathematik 2"),
            is_completed=False,
        ),
        Subject(
            name="Statistik 2",
            ects=3,
            semester="Semester 2",
            moodle_link=_moodle_link("Statistik 2"),
            is_completed=False,
        ),
        Subject(
            name="Geschäftsprozessmanagement",
            ects=6,
            semester="Semester 2",
            moodle_link=_moodle_link("Geschäftsprozessmanagement"),
            is_completed=False,
        ),
        Subject(
            name="Requirements Engineering",
            ects=6,
            semester="Semester 2",
            moodle_link=_moodle_link("Requirements Engineering"),
            is_completed=False,
        ),
        Subject(
            name="Objektorientierte Programmierung",
            ects=6,
            semester="Semester 2",
            moodle_link=_moodle_link("Objektorientierte Programmierung"),
            is_completed=False,
        ),
        Subject(
            name="Wahlmodul Semester 2",
            ects=3,
            semester="Semester 2",
            moodle_link=_moodle_link("Wahlmodul Semester 2"),
            is_completed=False,
        ),

        # Semester 3
        Subject(
            name="Ethik & Technik",
            ects=3,
            semester="Semester 3",
            moodle_link=_moodle_link("Ethik & Technik"),
            is_completed=False,
        ),
        Subject(
            name="Finanzmanagement",
            ects=3,
            semester="Semester 3",
            moodle_link=_moodle_link("Finanzmanagement"),
            is_completed=False,
        ),
        Subject(
            name="Digital Marketing",
            ects=3,
            semester="Semester 3",
            moodle_link=_moodle_link("Digital Marketing"),
            is_completed=False,
        ),
        Subject(
            name="Organisational Behaviour",
            ects=3,
            semester="Semester 3",
            moodle_link=_moodle_link("Organisational Behaviour"),
            is_completed=False,
        ),
        Subject(
            name="IT Projektmanagement",
            ects=3,
            semester="Semester 3",
            moodle_link=_moodle_link("IT Projektmanagement"),
            is_completed=False,
        ),
        Subject(
            name="Webbasierte Anwendungen",
            ects=6,
            semester="Semester 3",
            moodle_link=_moodle_link("Webbasierte Anwendungen"),
            is_completed=False,
        ),
        Subject(
            name="Datenbanktechnologien",
            ects=6,
            semester="Semester 3",
            moodle_link=_moodle_link("Datenbanktechnologien"),
            is_completed=False,
        ),
        Subject(
            name="Wahlmodul Semester 3",
            ects=3,
            semester="Semester 3",
            moodle_link=_moodle_link("Wahlmodul Semester 3"),
            is_completed=False,
        ),

        # Semester 4
        Subject(
            name="Topics in Business Information Technology",
            ects=6,
            semester="Semester 4",
            moodle_link=_moodle_link("Topics in Business Information Technology"),
            is_completed=False,
        ),
        Subject(
            name="Corporate Finance Basics",
            ects=3,
            semester="Semester 4",
            moodle_link=_moodle_link("Corporate Finance Basics"),
            is_completed=False,
        ),
        Subject(
            name="Supply Chain Management",
            ects=3,
            semester="Semester 4",
            moodle_link=_moodle_link("Supply Chain Management"),
            is_completed=False,
        ),
        Subject(
            name="IT-Recht",
            ects=3,
            semester="Semester 4",
            moodle_link=_moodle_link("IT-Recht"),
            is_completed=False,
        ),
        Subject(
            name="Betriebliche IT-Systeme",
            ects=3,
            semester="Semester 4",
            moodle_link=_moodle_link("Betriebliche IT-Systeme"),
            is_completed=False,
        ),
        Subject(
            name="Business Intelligence",
            ects=6,
            semester="Semester 4",
            moodle_link=_moodle_link("Business Intelligence"),
            is_completed=False,
        ),
        Subject(
            name="IT Security",
            ects=3,
            semester="Semester 4",
            moodle_link=_moodle_link("IT Security"),
            is_completed=False,
        ),
        Subject(
            name="Wahlmodul Semester 4",
            ects=3,
            semester="Semester 4",
            moodle_link=_moodle_link("Wahlmodul Semester 4"),
            is_completed=False,
        ),

        # Semester 5
        Subject(
            name="Praxisprojekt",
            ects=9,
            semester="Semester 5",
            moodle_link=_moodle_link("Praxisprojekt"),
            is_completed=False,
        ),
        Subject(
            name="Fachmodul Semester 5 - 1",
            ects=6,
            semester="Semester 5",
            moodle_link=_moodle_link("Fachmodul Semester 5 1"),
            is_completed=False,
        ),
        Subject(
            name="Fachmodul Semester 5 - 2",
            ects=6,
            semester="Semester 5",
            moodle_link=_moodle_link("Fachmodul Semester 5 2"),
            is_completed=False,
        ),
        Subject(
            name="Fachmodul Semester 5 - 3",
            ects=6,
            semester="Semester 5",
            moodle_link=_moodle_link("Fachmodul Semester 5 3"),
            is_completed=False,
        ),
        Subject(
            name="Wahlmodul Semester 5",
            ects=3,
            semester="Semester 5",
            moodle_link=_moodle_link("Wahlmodul Semester 5"),
            is_completed=False,
        ),

        # Semester 6
        Subject(
            name="Bachelor Thesis",
            ects=12,
            semester="Semester 6",
            moodle_link=_moodle_link("Bachelor Thesis"),
            is_completed=False,
        ),
        Subject(
            name="Fachmodul Semester 6 - 1",
            ects=6,
            semester="Semester 6",
            moodle_link=_moodle_link("Fachmodul Semester 6 1"),
            is_completed=False,
        ),
        Subject(
            name="Fachmodul Semester 6 - 2",
            ects=6,
            semester="Semester 6",
            moodle_link=_moodle_link("Fachmodul Semester 6 2"),
            is_completed=False,
        ),
        Subject(
            name="Fachmodul Semester 6 - 3",
            ects=6,
            semester="Semester 6",
            moodle_link=_moodle_link("Fachmodul Semester 6 3"),
            is_completed=False,
        ),
    ]

    for subject in subjects:
        session.add(subject)

    session.commit()

    saved_subjects = list(session.exec(select(Subject)))
    subject_map = {subject.name: subject.id for subject in saved_subjects if subject.id is not None}

    today = date.today()

    tasks = [
        Task(
            title="Prepare presentation for Communication Essentials",
            deadline=today + timedelta(days=3),
            planned_date=today + timedelta(days=1),
            estimated_minutes=60,
            priority="medium",
            notes="Focus on clear structure and concise speaking points.",
            subject_id=subject_map.get("Communication Essentials"),
        ),
        Task(
            title="Solve exercise sheet for Angewandte Mathematik 2",
            deadline=today + timedelta(days=4),
            planned_date=today + timedelta(days=2),
            estimated_minutes=90,
            priority="high",
            notes="Review functions and problem-solving methods.",
            subject_id=subject_map.get("Angewandte Mathematik 2"),
        ),
        Task(
            title="Review probability and statistics tasks",
            deadline=today + timedelta(days=5),
            planned_date=today + timedelta(days=3),
            estimated_minutes=75,
            priority="medium",
            notes="Focus on interpretation of results and formulas.",
            subject_id=subject_map.get("Statistik 2"),
        ),
        Task(
            title="Document a business process example",
            deadline=today + timedelta(days=6),
            planned_date=today + timedelta(days=4),
            estimated_minutes=80,
            priority="medium",
            notes="Describe the workflow and identify optimization potential.",
            subject_id=subject_map.get("Geschäftsprozessmanagement"),
        ),
        Task(
            title="Write stakeholder requirements draft",
            deadline=today + timedelta(days=7),
            planned_date=today + timedelta(days=5),
            estimated_minutes=95,
            priority="high",
            notes="Include functional and non-functional requirements.",
            subject_id=subject_map.get("Requirements Engineering"),
        ),
        Task(
            title="Finish OOP implementation task",
            deadline=today + timedelta(days=3),
            planned_date=today + timedelta(days=2),
            estimated_minutes=120,
            priority="high",
            notes="Complete class design and test object interactions.",
            subject_id=subject_map.get("Objektorientierte Programmierung"),
        ),
        Task(
            title="Plan topic for semester 2 elective",
            deadline=today + timedelta(days=8),
            planned_date=today + timedelta(days=6),
            estimated_minutes=45,
            priority="low",
            notes="Clarify expectations and prepare the first materials.",
            subject_id=subject_map.get("Wahlmodul Semester 2"),
        ),
    ]

    for task in tasks:
        session.add(task)

    session.commit()
