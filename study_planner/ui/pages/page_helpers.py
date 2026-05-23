from datetime import date


def get_subject_name_map(subjects) -> dict[int, str]:
    return {
        subject.id: subject.name
        for subject in subjects
        if subject.id is not None
    }


def get_dashboard_subject_ids(subjects, selected_semester: str) -> set[int]:
    if selected_semester == "All semesters":
        return {subject.id for subject in subjects if subject.id is not None}

    return {
        subject.id
        for subject in subjects
        if subject.id is not None and subject.semester == selected_semester
    }


def get_filtered_dashboard_tasks(tasks, subjects, selected_semester: str) -> list:
    subject_ids = get_dashboard_subject_ids(subjects, selected_semester)
    return [task for task in tasks if task.subject_id in subject_ids]


def get_statistics_subjects(subjects, selected_semester: str):
    if selected_semester == "All semesters":
        return subjects
    return [subject for subject in subjects if subject.semester == selected_semester]


def get_statistics_tasks(tasks, subjects, selected_semester: str):
    filtered_subjects = get_statistics_subjects(subjects, selected_semester)
    subject_ids = {subject.id for subject in filtered_subjects if subject.id is not None}
    return [task for task in tasks if task.subject_id in subject_ids]


def build_optional_date(
    day_value: str | None,
    month_value: str | None,
    year_value: str | None,
) -> date | None:
    if not day_value and not month_value and not year_value:
        return None

    if not day_value or not month_value or not year_value:
        raise ValueError("Incomplete date")

    return date(int(year_value), int(month_value), int(day_value))
