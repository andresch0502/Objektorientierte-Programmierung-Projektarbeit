import csv
from datetime import date

from study_planner.domain.models import Subject, Task
from study_planner.services.export_service import ExportService


def read_csv_rows(path):
    with open(path, newline="", encoding="utf-8-sig") as file:
        return list(csv.reader(file, delimiter=";"))


def test_export_subjects_to_csv_writes_header_and_subject_rows(tmp_path):
    service = ExportService()
    subjects = [
        Subject(id=1, name="Programming", ects=6, semester="Semester 1", moodle_link="https://moodle.example.com/programming", is_completed=True),
        Subject(id=2, name="Databases", ects=5, semester="Semester 2", moodle_link="", is_completed=False),
    ]
    output_path = tmp_path / "exports" / "subjects.csv"

    result_path = service.export_subjects_to_csv(subjects, str(output_path))
    rows = read_csv_rows(result_path)

    assert result_path == str(output_path)
    assert rows[0] == ["ID", "Subject Name", "ECTS", "Semester", "Moodle Link", "Completed"]
    assert rows[1] == ["1", "Programming", "6", "Semester 1", "https://moodle.example.com/programming", "Yes"]
    assert rows[2] == ["2", "Databases", "5", "Semester 2", "", "No"]


def test_export_tasks_to_csv_writes_subject_name_and_dates(tmp_path):
    service = ExportService()
    subjects = [Subject(id=1, name="Programming")]
    tasks = [
        Task(
            id=10,
            title="Finish Python assignment",
            subject_id=1,
            deadline=date(2026, 5, 31),
            planned_date=date(2026, 5, 28),
            estimated_minutes=120,
            priority="high",
            is_completed=False,
            notes="OOP part",
        ),
        Task(id=11, title="General task", subject_id=None, is_completed=True),
    ]
    output_path = tmp_path / "exports" / "tasks.csv"

    result_path = service.export_tasks_to_csv(tasks, subjects, str(output_path))
    rows = read_csv_rows(result_path)

    assert rows[0] == [
        "ID",
        "Task Title",
        "Subject",
        "Deadline",
        "Planned Date",
        "Estimated Minutes",
        "Priority",
        "Completed",
        "Notes",
    ]
    assert rows[1] == ["10", "Finish Python assignment", "Programming", "31.05.2026", "28.05.2026", "120", "High", "No", "OOP part"]
    assert rows[2] == ["11", "General task", "No subject", "", "", "0", "Medium", "Yes", ""]
