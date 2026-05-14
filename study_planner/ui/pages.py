from datetime import datetime

from nicegui import ui

from study_planner.ui.controllers import (
    add_study_session,
    add_subject,
    add_task,
    complete_task,
    get_app_title,
    get_study_sessions,
    get_subjects,
    get_task_progress,
    get_tasks,
    get_urgent_tasks,
)


def show_home_page() -> None:
    ui.label(get_app_title())

    ui.label("Subjects")

    name_input = ui.input("Subject name")
    description_input = ui.input("Description")

    subject_list = ui.column()

    task_title_input = ui.input("Task title")
    task_description_input = ui.input("Task description")
    deadline_input = ui.input("Deadline (YYYY-MM-DD)")
    subject_select = ui.select(options={}, label="Subject")

    session_date_input = ui.input("Session date (YYYY-MM-DD)")
    duration_input = ui.input("Duration in minutes")
    session_notes_input = ui.input("Session notes")
    session_subject_select = ui.select(options={}, label="Session subject")

    progress_box = ui.column()
    urgent_task_list = ui.column()
    task_list = ui.column()
    session_list = ui.column()

    def refresh_subject_list() -> None:
        subject_list.clear()
        with subject_list:
            subjects = get_subjects()
            for subject in subjects:
                ui.label(subject.name)

    def refresh_subject_options() -> None:
        subjects = get_subjects()
        options = {
            subject.id: subject.name
            for subject in subjects
            if subject.id is not None
        }
        subject_select.options = options
        session_subject_select.options = options
        subject_select.update()
        session_subject_select.update()

    def refresh_progress_box() -> None:
        progress_box.clear()
        with progress_box:
            progress = get_task_progress()
            ui.label(f"Total tasks: {progress['total']}")
            ui.label(f"Completed tasks: {progress['completed']}")
            ui.label(f"Open tasks: {progress['open']}")

    def refresh_urgent_task_list() -> None:
        urgent_task_list.clear()
        with urgent_task_list:
            urgent_tasks = get_urgent_tasks()
            if not urgent_tasks:
                ui.label("No urgent tasks at the moment.")
            for task in urgent_tasks:
                ui.label(f"{task.title} (Deadline: {task.deadline})")

    def refresh_task_list() -> None:
        task_list.clear()
        with task_list:
            tasks = get_tasks()
            for task in tasks:
                with ui.row():
                    deadline_text = f" (Deadline: {task.deadline})" if task.deadline else ""
                    status_text = "✅ " if task.is_completed else ""
                    ui.label(f"{status_text}{task.title}{deadline_text}")

                    if not task.is_completed and task.id is not None:
                        ui.button(
                            "Complete",
                            on_click=lambda task_id=task.id: handle_complete_task(task_id),
                        )

    def refresh_session_list() -> None:
        session_list.clear()
        with session_list:
            sessions = get_study_sessions()
            if not sessions:
                ui.label("No study sessions planned yet.")
            for study_session in sessions:
                ui.label(
                    f"{study_session.session_date} - {study_session.duration_minutes} min"
                    f" - {study_session.notes}"
                )

    def handle_add_subject() -> None:
        if not name_input.value:
            ui.notify("Please enter a subject name.")
            return

        add_subject(name_input.value, description_input.value or "")
        name_input.value = ""
        description_input.value = ""
        refresh_subject_list()
        refresh_subject_options()

    def handle_add_task() -> None:
        if not task_title_input.value:
            ui.notify("Please enter a task title.")
            return

        deadline = None
        if deadline_input.value:
            try:
                deadline = datetime.strptime(deadline_input.value, "%Y-%m-%d").date()
            except ValueError:
                ui.notify("Please use the date format YYYY-MM-DD.")
                return

        add_task(
            task_title_input.value,
            task_description_input.value or "",
            deadline,
            subject_select.value,
        )
        task_title_input.value = ""
        task_description_input.value = ""
        deadline_input.value = ""
        subject_select.value = None
        refresh_task_list()
        refresh_urgent_task_list()
        refresh_progress_box()

    def handle_complete_task(task_id: int) -> None:
        complete_task(task_id)
        refresh_task_list()
        refresh_urgent_task_list()
        refresh_progress_box()

    def handle_add_study_session() -> None:
        if not session_date_input.value:
            ui.notify("Please enter a session date.")
            return

        if not duration_input.value:
            ui.notify("Please enter a duration in minutes.")
            return

        try:
            session_date = datetime.strptime(session_date_input.value, "%Y-%m-%d").date()
        except ValueError:
            ui.notify("Please use the date format YYYY-MM-DD.")
            return

        try:
            duration_minutes = int(duration_input.value)
            if duration_minutes <= 0:
                ui.notify("Duration must be greater than 0.")
                return
        except ValueError:
            ui.notify("Please enter a valid number of minutes.")
            return

        add_study_session(
            session_date,
            duration_minutes,
            session_notes_input.value or "",
            session_subject_select.value,
        )
        session_date_input.value = ""
        duration_input.value = ""
        session_notes_input.value = ""
        session_subject_select.value = None
        refresh_session_list()

    ui.button("Add subject", on_click=handle_add_subject)

    refresh_subject_list()
    refresh_subject_options()

    ui.separator()
    ui.label("Progress")
    refresh_progress_box()

    ui.separator()
    ui.label("Urgent Tasks")
    refresh_urgent_task_list()

    ui.separator()
    ui.label("Tasks")
    ui.button("Add task", on_click=handle_add_task)
    refresh_task_list()

    ui.separator()
    ui.label("Study Sessions")
    ui.button("Add study session", on_click=handle_add_study_session)
    refresh_session_list()
