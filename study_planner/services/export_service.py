import csv
from pathlib import Path

from study_planner.domain.models import Subject, Task


class ExportService:
    def export_subjects_to_csv(self, subjects: list[Subject], output_path: str) -> str:
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        with path.open("w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["id", "name", "ects", "semester", "moodle_link", "is_completed"])

            for subject in subjects:
                writer.writerow([
                    subject.id,
                    subject.name,
                    subject.ects,
                    subject.semester,
                    subject.moodle_link,
                    subject.is_completed,
                ])

        return str(path)

    def export_tasks_to_csv(self, tasks: list[Task], output_path: str) -> str:
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        with path.open("w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow([
                "id",
                "title",
                "deadline",
                "planned_date",
                "estimated_minutes",
                "priority",
                "is_completed",
                "notes",
                "subject_id",
            ])

            for task in tasks:
                writer.writerow([
                    task.id,
                    task.title,
                    task.deadline,
                    task.planned_date,
                    task.estimated_minutes,
                    task.priority,
                    task.is_completed,
                    task.notes,
                    task.subject_id,
                ])

        return str(path)
