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

    with ui.column().style("max-width: 1200px; margin: 0 auto; padding: 24px; width: 100%; gap: 20px;"):
        ui.label(get_app_title()).classes("text-3xl font-bold")
        ui.label("Plan subjects, tasks, deadlines, and study sessions.").classes("text-gray-600")

        def section_title(title: str, subtitle: str = "") -> None:
            ui.label(title).classes("text-xl font-semibold")
            if subtitle:
                ui.label(subtitle).classes("text-sm text-gray-500")

        with ui.tabs().classes("w-full") as tabs:
            dashboard_tab = ui.tab("Dashboard")
            subjects_tab = ui.tab("Subjects")
            tasks_tab = ui.tab("Tasks")
            sessions_tab = ui.tab("Study Sessions")

        with ui.tab_panels(tabs, value=dashboard_tab).classes("w-full"):
            with ui.tab_panel(dashboard_tab):
                progress_box = ui.column().classes("w-full")
                urgent_task_list = ui.column().classes("w-full")
                study_statistics_box = ui.column().classes("w-full")

            with ui.tab_panel(subjects_tab):
                with ui.card().classes("w-full"):
                    section_title("Add New Subject")
                    subject_name_input = ui.input("Subject name").classes("w-full")
                    add_subject_button = ui.button("Add subject").classes("w-full")

                with ui.card().classes("w-full"):
                    section_title("Existing Subjects")
                    subject_list = ui.column().classes("w-full")

            with ui.tab_panel(tasks_tab):
                with ui.card().classes("w-full"):
                    section_title("Add Task", "Select a subject and add a task with optional notes.")
                    task_subject_select = ui.select(options={}, label="Subject").classes("w-full")
                    task_title_input = ui.input("Task title").classes("w-full")
                    deadline_input = ui.input("Deadline (YYYY-MM-DD)").classes("w-full")
                    task_notes_input = ui.textarea("Notes (optional)").classes("w-full")
                    add_task_button = ui.button("Add task").classes("w-full")

                with ui.card().classes("w-full"):
                    section_title("Task Overview")
                    task_list = ui.column().classes("w-full")

            with ui.tab_panel(sessions_tab):
                with ui.card().classes("w-full"):
                    section_title("Add Study Session", "Select a subject and enter date, duration, and optional notes.")
                    session_subject_select = ui.select(options={}, label="Subject").classes("w-full")
                    session_date_input = ui.input("Session date (YYYY-MM-DD)").classes("w-full")
                    duration_input = ui.input("Duration in minutes").classes("w-full")
                    session_notes_input = ui.textarea("Notes (optional)").classes("w-full")
                    add_session_button = ui.button("Add study session").classes("w-full")

                with ui.card().classes("w-full"):
                    section_title("Planned Study Sessions")
                    session_list = ui.column().classes("w-full")

        def get_subject_name_map() -> dict[int, str]:
            return {
                subject.id: subject.name
                for subject in get_subjects()
                if subject.id is not None
            }

        def refresh_subject_options() -> None:
            options = get_subject_name_map()
            task_subject_select.options = options
            session_subject_select.options = options
            task_subject_select.update()
            session_subject_select.update()

        def refresh_subject_list() -> None:
            subject_list.clear()
            with subject_list:
                subjects = get_subjects()
                if not subjects:
                    ui.label("No subjects added yet.").classes("text-gray-500")
                    return

                for subject in subjects:
                    with ui.card().classes("w-full"):
                        ui.label(subject.name).classes("font-medium")

        def refresh_progress_box() -> None:
            progress_box.clear()
            with progress_box:
                section_title("Progress")
                progress = get_task_progress()

                with ui.row().classes("w-full"):
                    with ui.card().style("flex: 1;"):
                        ui.label("Total tasks").classes("text-sm text-gray-500")
                        ui.label(str(progress["total"])).classes("text-2xl font-bold")

                    with ui.card().style("flex: 1;"):
                        ui.label("Completed").classes("text-sm text-gray-500")
                        ui.label(str(progress["completed"])).classes("text-2xl font-bold")

                    with ui.card().style("flex: 1;"):
                        ui.label("Open").classes("text-sm text-gray-500")
                        ui.label(str(progress["open"])).classes("text-2xl font-bold")

        def refresh_urgent_task_list() -> None:
            urgent_task_list.clear()
            with urgent_task_list:
                section_title("Urgent Tasks")
                urgent_tasks = get_urgent_tasks()
                subject_names = get_subject_name_map()

                if not urgent_tasks:
                    ui.label("No urgent tasks at the moment.").classes("text-gray-500")
                    return

                for task in urgent_tasks:
                    with ui.card().classes("w-full"):
                        ui.label(task.title).classes("font-medium")
                        if task.subject_id in subject_names:
                            ui.label(f"Subject: {subject_names[task.subject_id]}").classes("text-sm text-gray-600")
                        if task.deadline:
                            ui.label(f"Deadline: {task.deadline}").classes("text-sm text-red-600")
                        if task.notes:
                            ui.label(task.notes).classes("text-sm text-gray-500")

        def refresh_task_list() -> None:
            task_list.clear()
            with task_list:
                tasks = get_tasks()
                subject_names = get_subject_name_map()

                if not tasks:
                    ui.label("No tasks added yet.").classes("text-gray-500")
                    return

                for task in tasks:
                    with ui.card().classes("w-full"):
                        with ui.row().style("width: 100%; justify-content: space-between; align-items: start; gap: 12px;"):
                            with ui.column().classes("gap-1"):
                                title_prefix = "✅ " if task.is_completed else ""
                                ui.label(f"{title_prefix}{task.title}").classes("font-medium")

                                if task.subject_id in subject_names:
                                    ui.label(f"Subject: {subject_names[task.subject_id]}").classes("text-sm text-gray-600")

                                if task.deadline:
                                    ui.label(f"Deadline: {task.deadline}").classes("text-sm text-gray-600")

                                if task.notes:
                                    ui.label(task.notes).classes("text-sm text-gray-500")

                            if not task.is_completed and task.id is not None:
                                ui.button(
                                    "Complete",
                                    on_click=lambda task_id=task.id: handle_complete_task(task_id),
                                )

        def refresh_session_list() -> None:
            session_list.clear()
            with session_list:
                sessions = get_study_sessions()
                subject_names = get_subject_name_map()

                if not sessions:
                    ui.label("No study sessions planned yet.").classes("text-gray-500")
                    return

                for study_session in sessions:
                    with ui.card().classes("w-full"):
                        ui.label(f"{study_session.session_date}").classes("font-medium")
                        if study_session.subject_id in subject_names:
                            ui.label(f"Subject: {subject_names[study_session.subject_id]}").classes("text-sm text-gray-600")
                        ui.label(f"Duration: {study_session.duration_minutes} minutes").classes("text-sm text-gray-600")
                        if study_session.notes:
                            ui.label(study_session.notes).classes("text-sm text-gray-500")

        def refresh_study_statistics_box() -> None:
            study_statistics_box.clear()
            with study_statistics_box:
                section_title("Study Statistics")
                statistics = get_study_statistics()

                with ui.row().classes("w-full"):
                    with ui.card().style("flex: 1;"):
                        ui.label("Study sessions").classes("text-sm text-gray-500")
                        ui.label(str(statistics["total_sessions"])).classes("text-2xl font-bold")

                    with ui.card().style("flex: 1;"):
                        ui.label("Study minutes").classes("text-sm text-gray-500")
                        ui.label(str(statistics["total_minutes"])).classes("text-2xl font-bold")

        def refresh_dashboard() -> None:
            refresh_progress_box()
            refresh_urgent_task_list()
            refresh_study_statistics_box()

        def handle_add_subject() -> None:
            if not subject_name_input.value:
                ui.notify("Please enter a subject name.")
                return

            add_subject(subject_name_input.value)
            subject_name_input.value = ""
            refresh_subject_list()
            refresh_subject_options()
            ui.notify("Subject added.")

        def handle_add_task() -> None:
            if not task_subject_select.value:
                ui.notify("Please select a subject.")
                return

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
                deadline,
                task_notes_input.value or "",
                task_subject_select.value,
            )
            task_title_input.value = ""
            deadline_input.value = ""
            task_notes_input.value = ""
            task_subject_select.value = None
            refresh_task_list()
            refresh_dashboard()
            ui.notify("Task added.")

        def handle_complete_task(task_id: int) -> None:
            complete_task(task_id)
            refresh_task_list()
            refresh_dashboard()
            ui.notify("Task completed.")

        def handle_add_study_session() -> None:
            if not session_subject_select.value:
                ui.notify("Please select a subject.")
                return

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
            refresh_dashboard()
            ui.notify("Study session added.")

        add_subject_button.on("click", lambda: handle_add_subject())
        add_task_button.on("click", lambda: handle_add_task())
        add_session_button.on("click", lambda: handle_add_study_session())

        refresh_subject_options()
        refresh_subject_list()
        refresh_task_list()
        refresh_session_list()
        refresh_dashboard()
