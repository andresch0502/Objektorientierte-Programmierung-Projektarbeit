from datetime import datetime

from nicegui import ui

from study_planner.ui.controllers import (
    add_study_session,
    add_subject,
    add_task,
    complete_task,
    get_app_title,
    get_study_sessions,
    get_study_statistics,
    get_subjects,
    get_task_progress,
    get_tasks,
    get_urgent_tasks,
)


def show_home_page() -> None:
    ui.query("body").style("background-color: #f5f7fb;")

    with ui.column().style("max-width: 1400px; margin: 0 auto; padding: 24px; gap: 20px; width: 100%;"):
        ui.label(get_app_title()).classes("text-3xl font-bold")
        ui.label("Organize subjects, tasks, deadlines, and study sessions in one place.").classes("text-gray-600")

        name_input = ui.input("Subject name").classes("w-full")
        description_input = ui.input("Description").classes("w-full")

        task_title_input = ui.input("Task title").classes("w-full")
        task_description_input = ui.input("Task description").classes("w-full")
        deadline_input = ui.input("Deadline (YYYY-MM-DD)").classes("w-full")
        subject_select = ui.select(options={}, label="Subject").classes("w-full")

        session_date_input = ui.input("Session date (YYYY-MM-DD)").classes("w-full")
        duration_input = ui.input("Duration in minutes").classes("w-full")
        session_notes_input = ui.input("Session notes").classes("w-full")
        session_subject_select = ui.select(options={}, label="Session subject").classes("w-full")

        progress_box = ui.column().classes("w-full")
        urgent_task_list = ui.column().classes("w-full")
        subject_list = ui.column().classes("w-full")
        task_list = ui.column().classes("w-full")
        session_list = ui.column().classes("w-full")
        study_statistics_box = ui.column().classes("w-full")

        def section_title(title: str, subtitle: str = "") -> None:
            ui.label(title).classes("text-xl font-semibold")
            if subtitle:
                ui.label(subtitle).classes("text-sm text-gray-500")

        def refresh_subject_list() -> None:
            subject_list.clear()
            with subject_list:
                subjects = get_subjects()
                if not subjects:
                    ui.label("No subjects added yet.").classes("text-gray-500")
                    return

                for subject in subjects:
                    with ui.card().style("width: 100%;"):
                        ui.label(subject.name).classes("font-medium")
                        if subject.description:
                            ui.label(subject.description).classes("text-sm text-gray-600")

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

                with ui.row().style("width: 100%; gap: 12px; flex-wrap: wrap;"):
                    with ui.card().style("flex: 1; min-width: 180px;"):
                        ui.label("Total Tasks").classes("text-sm text-gray-500")
                        ui.label(str(progress["total"])).classes("text-2xl font-bold")

                    with ui.card().style("flex: 1; min-width: 180px;"):
                        ui.label("Completed").classes("text-sm text-gray-500")
                        ui.label(str(progress["completed"])).classes("text-2xl font-bold")

                    with ui.card().style("flex: 1; min-width: 180px;"):
                        ui.label("Open").classes("text-sm text-gray-500")
                        ui.label(str(progress["open"])).classes("text-2xl font-bold")

        def refresh_urgent_task_list() -> None:
            urgent_task_list.clear()
            with urgent_task_list:
                urgent_tasks = get_urgent_tasks()
                if not urgent_tasks:
                    ui.label("No urgent tasks at the moment.").classes("text-gray-500")
                    return

                for task in urgent_tasks:
                    with ui.card().style("width: 100%;"):
                        ui.label(task.title).classes("font-medium")
                        if task.deadline:
                            ui.label(f"Deadline: {task.deadline}").classes("text-sm text-red-600")

        def refresh_task_list() -> None:
            task_list.clear()
            with task_list:
                tasks = get_tasks()
                if not tasks:
                    ui.label("No tasks added yet.").classes("text-gray-500")
                    return

                for task in tasks:
                    with ui.card().style("width: 100%;"):
                        with ui.row().style("width: 100%; justify-content: space-between; align-items: center; gap: 12px;"):
                            with ui.column().classes("gap-1"):
                                title_prefix = "✅ " if task.is_completed else ""
                                ui.label(f"{title_prefix}{task.title}").classes("font-medium")

                                if task.description:
                                    ui.label(task.description).classes("text-sm text-gray-600")

                                if task.deadline:
                                    ui.label(f"Deadline: {task.deadline}").classes("text-sm text-gray-500")

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
                    ui.label("No study sessions planned yet.").classes("text-gray-500")
                    return

                for study_session in sessions:
                    with ui.card().style("width: 100%;"):
                        ui.label(f"{study_session.session_date}").classes("font-medium")
                        ui.label(f"Duration: {study_session.duration_minutes} minutes").classes("text-sm text-gray-600")
                        if study_session.notes:
                            ui.label(study_session.notes).classes("text-sm text-gray-500")

        def refresh_study_statistics_box() -> None:
            study_statistics_box.clear()
            with study_statistics_box:
                statistics = get_study_statistics()

                with ui.row().style("width: 100%; gap: 12px; flex-wrap: wrap;"):
                    with ui.card().style("flex: 1; min-width: 180px;"):
                        ui.label("Study Sessions").classes("text-sm text-gray-500")
                        ui.label(str(statistics["total_sessions"])).classes("text-2xl font-bold")

                    with ui.card().style("flex: 1; min-width: 180px;"):
                        ui.label("Study Minutes").classes("text-sm text-gray-500")
                        ui.label(str(statistics["total_minutes"])).classes("text-2xl font-bold")

        def handle_add_subject() -> None:
            if not name_input.value:
                ui.notify("Please enter a subject name.")
                return

            add_subject(name_input.value, description_input.value or "")
            name_input.value = ""
            description_input.value = ""
            refresh_subject_list()
            refresh_subject_options()
            ui.notify("Subject added.")

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
            ui.notify("Task added.")

        def handle_complete_task(task_id: int) -> None:
            complete_task(task_id)
            refresh_task_list()
            refresh_urgent_task_list()
            refresh_progress_box()
            ui.notify("Task completed.")

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
            refresh_study_statistics_box()
            ui.notify("Study session added.")

        with ui.row().style("width: 100%; gap: 20px; align-items: flex-start; flex-wrap: wrap;"):
            with ui.column().style("flex: 1; min-width: 360px; gap: 20px;"):
                with ui.card().style("width: 100%;"):
                    section_title("Add Subject", "Create and organize your subjects.")
                    name_input
                    description_input
                    ui.button("Add subject", on_click=handle_add_subject).classes("w-full")

                with ui.card().style("width: 100%;"):
                    section_title("Add Task", "Create a task and optionally assign a subject and deadline.")
                    task_title_input
                    task_description_input
                    deadline_input
                    subject_select
                    ui.button("Add task", on_click=handle_add_task).classes("w-full")

                with ui.card().style("width: 100%;"):
                    section_title("Plan Study Session", "Add a learning session with date and duration.")
                    session_date_input
                    duration_input
                    session_notes_input
                    session_subject_select
                    ui.button("Add study session", on_click=handle_add_study_session).classes("w-full")

            with ui.column().style("flex: 1.4; min-width: 420px; gap: 20px;"):
                with ui.card().style("width: 100%;"):
                    section_title("Progress")
                    refresh_progress_box()

                with ui.card().style("width: 100%;"):
                    section_title("Urgent Tasks")
                    refresh_urgent_task_list()

                with ui.card().style("width: 100%;"):
                    section_title("Subjects")
                    refresh_subject_list()

                with ui.card().style("width: 100%;"):
                    section_title("Tasks")
                    refresh_task_list()

                with ui.card().style("width: 100%;"):
                    section_title("Study Sessions")
                    refresh_session_list()

                with ui.card().style("width: 100%;"):
                    section_title("Study Statistics")
                    refresh_study_statistics_box()

        refresh_subject_options()
