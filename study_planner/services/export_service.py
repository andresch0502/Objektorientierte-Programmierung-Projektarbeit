import csv
from pathlib import Path

from study_planner.domain.models import Subject, Task


class ExportService:
    def export_subjects_to_csv(self, subjects: list[Subject], output_path: str) -> str:
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        with path.open("w", newline="", encoding="utf-8-sig") as file:
            writer = csv.writer(file, delimiter=";")
            writer.writerow([
                "ID",
                "Subject Name",
                "ECTS",
                "Semester",
                "Moodle Link",
                "Completed",
            ])

            for subject in subjects:
                writer.writerow([
                    subject.id,
                    subject.name,
                    subject.ects,
                    subject.semester,
                    subject.moodle_link,
                    "Yes" if subject.is_completed else "No",
                ])

        return str(path)

    def export_tasks_to_csv(
        self,
        tasks: list[Task],
        subjects: list[Subject],
        output_path: str,
    ) -> str:
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        subject_map = {
            subject.id: subject.name
            for subject in subjects
            if subject.id is not None
        }

        with path.open("w", newline="", encoding="utf-8-sig") as file:
            writer = csv.writer(file, delimiter=";")
            writer.writerow([
                "ID",
                "Task Title",
                "Subject",
                "Deadline",
                "Planned Date",
                "Estimated Minutes",
                "Priority",
                "Completed",
                "Notes",
            ])

            for task in tasks:
                writer.writerow([
                    task.id,
                    task.title,
                    subject_map.get(task.subject_id, "No subject"),
                    task.deadline.strftime("%d.%m.%Y") if task.deadline else "",
                    task.planned_date.strftime("%d.%m.%Y") if task.planned_date else "",
                    task.estimated_minutes,
                    task.priority.capitalize(),
                    "Yes" if task.is_completed else "No",
                    task.notes,
                ])

        return str(path)
