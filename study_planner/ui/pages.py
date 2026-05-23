from datetime import date, timedelta

from nicegui import ui

from study_planner.ui.auth import get_logged_in_username, is_logged_in, login, logout
from study_planner.ui.controllers import (
    add_subject,
    add_task,
    complete_task,
    edit_subject,
    export_subjects_csv,
    export_tasks_csv,
    get_app_title,
    get_completed_subjects,
    get_credit_summary,
    get_priority_distribution,
    get_semester_statistics,
    get_subjects,
    get_tasks,
    get_tasks_per_subject,
    remove_subject,
)


def show_home_page() -> None:
    ui.query("body").style(
        "background: linear-gradient(180deg, #f8fafc 0%, #eef2ff 45%, #f8fafc 100%); "
        "min-height: 100vh;"
    )

    if not is_logged_in():
        def handle_login() -> None:
            username = username_input.value or ""
            password = password_input.value or ""

            if login(username, password):
                ui.notify("Login successful.")
                ui.navigate.reload()
            else:
                ui.notify("Invalid username or password.", color="negative")

        with ui.column().style(
            "min-height: 100vh; width: 100%; align-items: center; justify-content: center; padding: 28px;"
        ):
            with ui.card().style(
                "width: min(460px, 92vw); border-radius: 24px; padding: 28px; "
                "background: white; box-shadow: 0 18px 40px rgba(15, 23, 42, 0.12);"
            ):
                ui.label("🔐 StudyPlanner Login").classes("text-3xl font-bold text-slate-800")
                ui.label("Please log in to access your study planner.").classes("text-slate-500")
                username_input = ui.input("Username").classes("w-full")
                password_input = ui.input("Password", password=True, password_toggle_button=True).classes("w-full")
                ui.button("Log in", on_click=handle_login).classes("w-full").props("color=primary")
                with ui.card().style(
                    "width: 100%; margin-top: 8px; border-radius: 16px; padding: 14px; "
                    "background: #f8fafc; box-shadow: none;"
                ):
                    ui.label("Demo login").classes("text-sm font-semibold text-slate-700")
                    ui.label("Username: admin").classes("text-sm text-slate-600")
                    ui.label("Password: studyplanner123").classes("text-sm text-slate-600")
        return

    def handle_logout() -> None:
        logout()
        ui.notify("Logged out.")
        ui.navigate.reload()

    with ui.column().style(
        "max-width: 1280px; margin: 0 auto; padding: 28px; width: 100%; gap: 22px;"
    ):
        with ui.card().style(
            "width: 100%; border-radius: 24px; padding: 26px; "
            "background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%); "
            "color: white; box-shadow: 0 18px 40px rgba(79, 70, 229, 0.22);"
        ):
            with ui.row().style(
                "width: 100%; justify-content: space-between; align-items: flex-start; gap: 16px; flex-wrap: wrap;"
            ):
                with ui.column().classes("gap-2"):
                    ui.label(f"📚 {get_app_title()}").classes("text-4xl font-bold")
                    ui.label(
                        "Organize subjects, tasks, credits, and semester progress in one clear workspace."
                    ).classes("text-base opacity-90")
                    with ui.row().classes("w-full").style("gap: 10px; margin-top: 12px; flex-wrap: wrap;"):
                        ui.label("✨ Cleaner workflow").style(
                            "background: rgba(255,255,255,0.18); padding: 6px 12px; border-radius: 999px;"
                        )
                        ui.label("📊 Better statistics").style(
                            "background: rgba(255,255,255,0.18); padding: 6px 12px; border-radius: 999px;"
                        )
                        ui.label("🗓️ Weekly planning").style(
                            "background: rgba(255,255,255,0.18); padding: 6px 12px; border-radius: 999px;"
                        )

                with ui.column().style("align-items: flex-end; gap: 8px;"):
                    ui.label(f"Logged in as: {get_logged_in_username()}").classes("text-sm opacity-90")
                    ui.button("Logout", on_click=handle_logout).props("outline color=white")

        edit_subject_state = {"id": None}

        semester_options = [
            "All semesters",
            "Semester 1",
            "Semester 2",
            "Semester 3",
            "Semester 4",
            "Semester 5",
            "Semester 6",
        ]

        def section_title(title: str, subtitle: str = "") -> None:
            ui.label(title).classes("text-xl font-semibold text-slate-800")
            if subtitle:
                ui.label(subtitle).classes("text-sm text-slate-500")

        def card_style() -> str:
            return (
                "width: 100%; border-radius: 20px; padding: 18px; "
                "box-shadow: 0 10px 28px rgba(15, 23, 42, 0.08); "
                "border: 1px solid rgba(148, 163, 184, 0.15);"
            )

        def info_card(title: str, value: str, background: str, text_color: str = "#0f172a") -> None:
            with ui.card().style(
                f"flex: 1; min-width: 180px; border-radius: 18px; padding: 16px; "
                f"background: {background}; color: {text_color}; "
                "box-shadow: 0 10px 26px rgba(15, 23, 42, 0.08);"
            ):
                ui.label(title).classes("text-sm opacity-80")
                ui.label(value).classes("text-3xl font-bold")

        def priority_style(priority: str) -> str:
            mapping = {
                "high": "background:#fee2e2;color:#b91c1c;",
                "medium": "background:#fef3c7;color:#b45309;",
                "low": "background:#dcfce7;color:#15803d;",
            }
            base = "padding: 4px 10px; border-radius: 999px; font-size: 12px; font-weight: 600;"
            return base + mapping.get(priority, "background:#e2e8f0;color:#334155;")

        def status_style(is_completed: bool) -> str:
            if is_completed:
                return (
                    "padding: 4px 10px; border-radius: 999px; font-size: 12px; "
                    "font-weight: 600; background:#dcfce7; color:#15803d;"
                )
            return (
                "padding: 4px 10px; border-radius: 999px; font-size: 12px; "
                "font-weight: 600; background:#e2e8f0; color:#475569;"
            )

        with ui.tabs().classes("w-full") as tabs:
            dashboard_tab = ui.tab("🏠 Dashboard")
            subjects_tab = ui.tab("📚 Subjects")
            tasks_tab = ui.tab("📝 Tasks")
            statistics_tab = ui.tab("📊 Statistics")

        with ui.tab_panels(tabs, value=dashboard_tab).classes("w-full"):
            with ui.tab_panel(dashboard_tab):
                with ui.card().style(card_style()):
                    section_title("Semester View", "Filter the dashboard by semester.")
                    dashboard_semester_select = ui.select(
                        options=semester_options,
                        label="Semester filter",
                        value="All semesters",
                        on_change=lambda _: refresh_dashboard(),
                    ).classes("w-full max-w-xs")

                credit_box = ui.column().classes("w-full")
                progress_box = ui.column().classes("w-full")
                urgent_task_list = ui.column().classes("w-full")
                week_overview_box = ui.column().classes("w-full")

            with ui.tab_panel(subjects_tab):
                with ui.card().style(card_style()):
                    section_title("📚 Add New Subject", "Create a subject with credits, semester, and Moodle link.")
                    subject_name_input = ui.input("Subject name").classes("w-full")
                    subject_ects_input = ui.input("ECTS").classes("w-full")
                    subject_semester_select = ui.select(
                        options=semester_options[1:],
                        label="Semester",
                        value="Semester 1",
                    ).classes("w-full")
                    subject_moodle_link_input = ui.input("Moodle link (optional)").classes("w-full")
                    add_subject_button = ui.button("Add subject").classes("w-full").props("color=primary")

                with ui.card().style(card_style()):
                    section_title("🗂️ Existing Subjects", "Overview of all modules and their status.")
                    subject_list = ui.column().classes("w-full")

            with ui.tab_panel(tasks_tab):
                with ui.card().style(card_style()):
                    section_title(
                        "📝 Add Task",
                        "Mandatory: Subject, Task title, Priority. Optional: deadline, planned date, estimated minutes, notes.",
                    )

                    task_subject_select = ui.select(options={}, label="Subject *").classes("w-full")
                    task_title_input = ui.input("Task title *").classes("w-full")

                    priority_select = ui.select(
                        options={
                            "high": "High",
                            "medium": "Medium",
                            "low": "Low",
                        },
                        label="Priority *",
                        value="medium",
                    ).classes("w-full")

                    ui.label("Deadline (optional)").classes("text-sm text-slate-600")
                    with ui.row().classes("w-full").style("gap: 12px; flex-wrap: wrap;"):
                        deadline_day_select = ui.select(
                            options=[str(day) for day in range(1, 32)],
                            label="Day",
                        ).classes("w-full")
                        deadline_month_select = ui.select(
                            options=[str(month) for month in range(1, 13)],
                            label="Month",
                        ).classes("w-full")
                        deadline_year_select = ui.select(
                            options=[str(year) for year in range(2025, 2036)],
                            label="Year",
                        ).classes("w-full")

                    ui.label("Planned date (optional)").classes("text-sm text-slate-600")
                    with ui.row().classes("w-full").style("gap: 12px; flex-wrap: wrap;"):
                        planned_day_select = ui.select(
                            options=[str(day) for day in range(1, 32)],
                            label="Day",
                        ).classes("w-full")
                        planned_month_select = ui.select(
                            options=[str(month) for month in range(1, 13)],
                            label="Month",
                        ).classes("w-full")
                        planned_year_select = ui.select(
                            options=[str(year) for year in range(2025, 2036)],
                            label="Year",
                        ).classes("w-full")

                    estimated_minutes_input = ui.input("Estimated minutes (optional)").classes("w-full")
                    task_notes_input = ui.textarea("Notes (optional)").classes("w-full")
                    add_task_button = ui.button("Add task").classes("w-full").props("color=primary")

                with ui.card().style(card_style()):
                    section_title("✅ Task Overview", "All planned and completed tasks.")
                    task_list = ui.column().classes("w-full")

            with ui.tab_panel(statistics_tab):
                with ui.card().style(card_style()):
                    section_title("📤 Export", "Export subjects and tasks as CSV files for Excel.")
                    export_subjects_button = ui.button("Export Subjects CSV").classes("w-full").props("color=primary")
                    export_tasks_button = ui.button("Export Tasks CSV").classes("w-full").props("color=primary")

                with ui.card().style(card_style()):
                    section_title("🧮 Statistics Filter", "Limit charts and summary cards to a single semester.")
                    statistics_semester_select = ui.select(
                        options=semester_options,
                        label="Semester filter",
                        value="All semesters",
                        on_change=lambda _: refresh_statistics_box(),
                    ).classes("w-full max-w-xs")

                statistics_box = ui.column().classes("w-full")

        with ui.dialog() as edit_subject_dialog, ui.card().style(
            "width: min(560px, 90vw); border-radius: 22px; padding: 18px;"
        ):
            ui.label("✏️ Edit Subject").classes("text-xl font-semibold")
            edit_subject_name_input = ui.input("Subject name").classes("w-full")
            edit_subject_ects_input = ui.input("ECTS").classes("w-full")
            edit_subject_semester_select = ui.select(
                options=semester_options[1:],
                label="Semester",
                value="Semester 1",
            ).classes("w-full")
            edit_subject_moodle_link_input = ui.input("Moodle link (optional)").classes("w-full")
            edit_subject_completed_checkbox = ui.checkbox("Module completed")
            with ui.row().classes("w-full justify-end").style("gap: 10px;"):
                cancel_edit_subject_button = ui.button("Cancel")
                save_edit_subject_button = ui.button("Save changes").props("color=primary")

        def get_subject_name_map() -> dict[int, str]:
            return {
                subject.id: subject.name
                for subject in get_subjects()
                if subject.id is not None
            }

        def get_dashboard_subject_ids() -> set[int]:
            subjects = get_subjects()
            selected_semester = dashboard_semester_select.value or "All semesters"
            if selected_semester == "All semesters":
                return {subject.id for subject in subjects if subject.id is not None}
            return {
                subject.id
                for subject in subjects
                if subject.id is not None and subject.semester == selected_semester
            }

        def get_filtered_dashboard_tasks() -> list:
            subject_ids = get_dashboard_subject_ids()
            return [task for task in get_tasks() if task.subject_id in subject_ids]

        def get_statistics_subjects():
            selected_semester = statistics_semester_select.value or "All semesters"
            subjects = get_subjects()
            if selected_semester == "All semesters":
                return subjects
            return [subject for subject in subjects if subject.semester == selected_semester]

        def get_statistics_tasks():
            subjects = get_statistics_subjects()
            subject_ids = {subject.id for subject in subjects if subject.id is not None}
            tasks = get_tasks()
            return [task for task in tasks if task.subject_id in subject_ids]

        def build_optional_date(
            day_value: str | None,
            month_value: str | None,
            year_value: str | None,
            label: str,
        ) -> date | None:
            if not day_value and not month_value and not year_value:
                return None

            if not day_value or not month_value or not year_value:
                ui.notify(f"Please complete day, month, and year for the {label}.")
                raise ValueError(label)

            try:
                return date(int(year_value), int(month_value), int(day_value))
            except ValueError:
                ui.notify(f"Please select a valid {label}.")
                raise

        def refresh_subject_options() -> None:
            options = get_subject_name_map()
            task_subject_select.options = options
            task_subject_select.update()

        def open_edit_subject_dialog(subject_id: int) -> None:
            subjects = get_subjects()
            subject = next((item for item in subjects if item.id == subject_id), None)
            if subject is None:
                ui.notify("Subject not found.")
                return

            edit_subject_state["id"] = subject.id
            edit_subject_name_input.value = subject.name
            edit_subject_ects_input.value = str(subject.ects)
            edit_subject_semester_select.value = subject.semester
            edit_subject_moodle_link_input.value = subject.moodle_link
            edit_subject_completed_checkbox.value = subject.is_completed
            edit_subject_dialog.open()

        def refresh_subject_list() -> None:
            subject_list.clear()
            with subject_list:
                subjects = get_subjects()
                if not subjects:
                    ui.label("No subjects added yet.").classes("text-slate-500")
                    return

                for subject in subjects:
                    with ui.card().style(card_style()):
                        with ui.row().style(
                            "width: 100%; justify-content: space-between; align-items: flex-start; gap: 12px;"
                        ):
                            with ui.column().classes("gap-2"):
                                ui.label(subject.name).classes("text-lg font-semibold text-slate-800")
                                with ui.row().classes("items-center").style("gap: 8px; flex-wrap: wrap;"):
                                    ui.label(f"ECTS: {subject.ects}").style(
                                        "background:#eff6ff; color:#1d4ed8; padding:4px 10px; border-radius:999px; font-size:12px; font-weight:600;"
                                    )
                                    ui.label(subject.semester).style(
                                        "background:#f5f3ff; color:#6d28d9; padding:4px 10px; border-radius:999px; font-size:12px; font-weight:600;"
                                    )
                                    ui.label("Completed" if subject.is_completed else "Not completed").style(
                                        status_style(subject.is_completed)
                                    )
                                if subject.moodle_link:
                                    ui.link("Open Moodle", subject.moodle_link, new_tab=True).classes("text-sm")

                            with ui.row().classes("gap-2"):
                                if subject.id is not None:
                                    ui.button(
                                        "Edit",
                                        on_click=lambda subject_id=subject.id: open_edit_subject_dialog(subject_id),
                                    ).props("outline color=primary")
                                    ui.button(
                                        "Delete",
                                        on_click=lambda subject_id=subject.id: handle_remove_subject(subject_id),
                                    ).props("color=negative")

        def refresh_credit_box() -> None:
            credit_box.clear()
            with credit_box:
                selected_semester = dashboard_semester_select.value or "All semesters"
                section_title("🎓 Credits Overview", f"Showing credits for: {selected_semester}")
                credits = get_credit_summary(selected_semester)

                with ui.row().classes("w-full").style("gap: 14px; flex-wrap: wrap;"):
                    info_card("Planned Credits", str(credits["planned"]), "linear-gradient(135deg, #dbeafe 0%, #eff6ff 100%)", "#1e3a8a")
                    info_card("Completed Credits", str(credits["completed"]), "linear-gradient(135deg, #dcfce7 0%, #f0fdf4 100%)", "#166534")
                    info_card("Open Credits", str(credits["open"]), "linear-gradient(135deg, #fee2e2 0%, #fff1f2 100%)", "#9f1239")

        def refresh_progress_box() -> None:
            progress_box.clear()
            with progress_box:
                selected_semester = dashboard_semester_select.value or "All semesters"
                section_title("📈 Progress", f"Task status for: {selected_semester}")
                tasks = get_filtered_dashboard_tasks()

                total = len(tasks)
                completed = len([task for task in tasks if task.is_completed])
                open_tasks = total - completed

                with ui.row().classes("w-full").style("gap: 14px; flex-wrap: wrap;"):
                    info_card("Filtered tasks", str(total), "linear-gradient(135deg, #e0f2fe 0%, #f8fafc 100%)", "#0f172a")
                    info_card("Completed", str(completed), "linear-gradient(135deg, #dcfce7 0%, #f0fdf4 100%)", "#166534")
                    info_card("Open", str(open_tasks), "linear-gradient(135deg, #fef3c7 0%, #fffbeb 100%)", "#92400e")

        def refresh_urgent_task_list() -> None:
            urgent_task_list.clear()
            with urgent_task_list:
                selected_semester = dashboard_semester_select.value or "All semesters"
                section_title("⚠️ Urgent Tasks", f"Urgent tasks for: {selected_semester}")
                subject_names = get_subject_name_map()

                urgent_tasks = [
                    task
                    for task in get_filtered_dashboard_tasks()
                    if not task.is_completed and task.deadline is not None
                ]
                urgent_tasks = sorted(urgent_tasks, key=lambda task: task.deadline)[:3]

                if not urgent_tasks:
                    with ui.card().style(card_style()):
                        ui.label("No urgent tasks at the moment.").classes("text-slate-500")
                    return

                with ui.row().classes("w-full").style("gap: 14px; flex-wrap: wrap;"):
                    for task in urgent_tasks:
                        with ui.card().style(
                            "flex: 1; min-width: 260px; border-radius: 20px; padding: 16px; "
                            "box-shadow: 0 10px 28px rgba(15, 23, 42, 0.08); background: #ffffff;"
                        ):
                            ui.label(task.title).classes("text-lg font-semibold text-slate-800")
                            if task.subject_id in subject_names:
                                ui.label(f"Subject: {subject_names[task.subject_id]}").classes("text-sm text-slate-600")
                            with ui.row().classes("items-center").style("gap: 8px; margin-top: 8px; flex-wrap: wrap;"):
                                ui.label(task.priority.capitalize()).style(priority_style(task.priority))
                                if task.deadline:
                                    ui.label(f"Deadline: {task.deadline}").style(
                                        "background:#fee2e2;color:#b91c1c;padding:4px 10px;border-radius:999px;font-size:12px;font-weight:600;"
                                    )
                            if task.estimated_minutes:
                                ui.label(f"Planned effort: {task.estimated_minutes} minutes").classes("text-sm text-slate-600")
                            if task.notes:
                                ui.label(task.notes).classes("text-sm text-slate-500")

        def refresh_week_overview() -> None:
            week_overview_box.clear()
            with week_overview_box:
                selected_semester = dashboard_semester_select.value or "All semesters"
                section_title("🗓️ Weekly Calendar", f"Planned tasks for the next 7 days ({selected_semester})")

                tasks = get_filtered_dashboard_tasks()
                subject_names = get_subject_name_map()
                start_day = date.today()

                with ui.element("div").style(
                    "display: grid; grid-template-columns: repeat(7, minmax(150px, 1fr)); "
                    "gap: 12px; width: 100%;"
                ):
                    for offset in range(7):
                        current_day = start_day + timedelta(days=offset)
                        day_tasks = [task for task in tasks if task.planned_date == current_day]

                        with ui.card().style(
                            "min-height: 260px; width: 100%; border-radius: 18px; padding: 14px; "
                            "box-shadow: 0 10px 22px rgba(15, 23, 42, 0.08); background: #ffffff;"
                        ):
                            ui.label(current_day.strftime("%a")).classes("text-sm text-slate-500")
                            ui.label(current_day.strftime("%d.%m.%Y")).classes("font-semibold text-slate-800")

                            if not day_tasks:
                                ui.label("No tasks").classes("text-sm text-slate-400")
                                continue

                            for task in day_tasks:
                                subject_text = subject_names.get(task.subject_id, "No subject")

                                with ui.card().style(
                                    "width: 100%; margin-top: 8px; border-radius: 14px; "
                                    "padding: 10px; background: #f8fafc; box-shadow: none;"
                                ):
                                    ui.label(task.title).classes("text-sm font-medium text-slate-800")
                                    ui.label(subject_text).classes("text-xs text-slate-600")
                                    ui.label(task.priority.capitalize()).style(priority_style(task.priority))
                                    if task.estimated_minutes:
                                        ui.label(f"{task.estimated_minutes} min").classes("text-xs text-slate-600")
                                    if task.deadline:
                                        ui.label(f"Due: {task.deadline}").classes("text-xs text-red-600")

        def refresh_task_list() -> None:
            task_list.clear()
            with task_list:
                tasks = get_tasks()
                subject_names = get_subject_name_map()

                if not tasks:
                    ui.label("No tasks added yet.").classes("text-slate-500")
                    return

                for task in tasks:
                    with ui.card().style(card_style()):
                        with ui.row().style(
                            "width: 100%; justify-content: space-between; align-items: flex-start; gap: 12px;"
                        ):
                            with ui.column().classes("gap-2"):
                                title_prefix = "✅ " if task.is_completed else ""
                                ui.label(f"{title_prefix}{task.title}").classes("text-lg font-semibold text-slate-800")

                                with ui.row().classes("items-center").style("gap: 8px; flex-wrap: wrap;"):
                                    if task.subject_id in subject_names:
                                        ui.label(subject_names[task.subject_id]).style(
                                            "background:#eff6ff; color:#1d4ed8; padding:4px 10px; border-radius:999px; font-size:12px; font-weight:600;"
                                        )
                                    ui.label(task.priority.capitalize()).style(priority_style(task.priority))
                                    ui.label("Completed" if task.is_completed else "Open").style(
                                        status_style(task.is_completed)
                                    )

                                if task.deadline:
                                    ui.label(f"Deadline: {task.deadline}").classes("text-sm text-slate-600")

                                if task.planned_date:
                                    ui.label(f"Planned date: {task.planned_date}").classes("text-sm text-slate-600")

                                if task.estimated_minutes:
                                    ui.label(f"Estimated time: {task.estimated_minutes} minutes").classes("text-sm text-slate-600")

                                if task.notes:
                                    ui.label(task.notes).classes("text-sm text-slate-500")

                            if not task.is_completed and task.id is not None:
                                ui.button(
                                    "Complete",
                                    on_click=lambda task_id=task.id: handle_complete_task(task_id),
                                ).props("color=positive")

        def refresh_statistics_box() -> None:
            statistics_box.clear()
            with statistics_box:
                selected_semester = statistics_semester_select.value or "All semesters"
                section_title("📊 Statistics", f"Showing statistics for: {selected_semester}")

                tasks = get_statistics_tasks()
                subjects = get_statistics_subjects()
                tasks_per_subject = get_tasks_per_subject(selected_semester)
                priority_distribution = get_priority_distribution(selected_semester)
                semester_statistics = get_semester_statistics()
                completed_subjects = get_completed_subjects(selected_semester)

                if not tasks and not subjects:
                    with ui.card().style(card_style()):
                        ui.label("No statistics available yet.").classes("text-slate-500")
                    return

                with ui.row().classes("w-full").style("gap: 14px; flex-wrap: wrap;"):
                    info_card("Total Subjects", str(len(subjects)), "linear-gradient(135deg, #ede9fe 0%, #f5f3ff 100%)", "#5b21b6")
                    info_card("Total Tasks", str(len(tasks)), "linear-gradient(135deg, #e0f2fe 0%, #f8fafc 100%)", "#0f172a")
                    info_card("Planned Minutes", str(sum(task.estimated_minutes for task in tasks)), "linear-gradient(135deg, #fef3c7 0%, #fffbeb 100%)", "#92400e")

                with ui.row().classes("w-full").style("gap: 18px; flex-wrap: wrap;"):
                    with ui.card().style(
                        "flex: 1; min-width: 320px; border-radius: 20px; padding: 18px; "
                        "box-shadow: 0 10px 28px rgba(15, 23, 42, 0.08);"
                    ):
                        ui.label("Tasks per Subject").classes("text-lg font-semibold text-slate-800")
                        ui.echart({
                            "xAxis": {"type": "category", "data": [item["subject"] for item in tasks_per_subject]},
                            "yAxis": {"type": "value"},
                            "series": [{"type": "bar", "data": [item["count"] for item in tasks_per_subject]}],
                            "tooltip": {},
                        }).style("height: 350px; width: 100%;")

                    with ui.card().style(
                        "flex: 1; min-width: 320px; border-radius: 20px; padding: 18px; "
                        "box-shadow: 0 10px 28px rgba(15, 23, 42, 0.08);"
                    ):
                        ui.label("Priority Distribution").classes("text-lg font-semibold text-slate-800")
                        ui.echart({
                            "tooltip": {"trigger": "item"},
                            "series": [{
                                "type": "pie",
                                "radius": "65%",
                                "data": [
                                    {"value": priority_distribution["high"], "name": "High"},
                                    {"value": priority_distribution["medium"], "name": "Medium"},
                                    {"value": priority_distribution["low"], "name": "Low"},
                                ],
                            }],
                        }).style("height: 350px; width: 100%;")

                if selected_semester == "All semesters" and semester_statistics:
                    with ui.card().style(card_style()):
                        ui.label("Semester Credits").classes("text-lg font-semibold text-slate-800")
                        ui.echart({
                            "tooltip": {"trigger": "axis"},
                            "legend": {"data": ["Planned", "Completed"]},
                            "xAxis": {"type": "category", "data": [item["semester"] for item in semester_statistics]},
                            "yAxis": {"type": "value"},
                            "series": [
                                {"name": "Planned", "type": "bar", "data": [item["planned_credits"] for item in semester_statistics]},
                                {"name": "Completed", "type": "bar", "data": [item["completed_credits"] for item in semester_statistics]},
                            ],
                        }).style("height: 350px; width: 100%;")

                    ui.label("Semester Detail View").classes("text-lg font-semibold text-slate-800")
                    for item in semester_statistics:
                        with ui.card().style(card_style()):
                            ui.label(str(item["semester"])).classes("font-semibold text-slate-800")
                            ui.label(f"Modules: {item['modules']}").classes("text-sm text-slate-600")
                            ui.label(f"Completed modules: {item['completed_modules']}").classes("text-sm text-slate-600")
                            ui.label(f"Planned credits: {item['planned_credits']}").classes("text-sm text-slate-600")
                            ui.label(f"Completed credits: {item['completed_credits']}").classes("text-sm text-slate-600")

                ui.label("Tasks per Subject (Detail View)").classes("text-lg font-semibold text-slate-800")

                if not subjects:
                    ui.label("No subjects available.").classes("text-slate-500")
                else:
                    for subject in subjects:
                        subject_tasks = [task for task in tasks if task.subject_id == subject.id]
                        with ui.card().style(card_style()):
                            ui.label(subject.name).classes("text-lg font-semibold text-slate-800")
                            with ui.row().classes("items-center").style("gap: 8px; flex-wrap: wrap;"):
                                ui.label(f"ECTS: {subject.ects}").style(
                                    "background:#eff6ff; color:#1d4ed8; padding:4px 10px; border-radius:999px; font-size:12px; font-weight:600;"
                                )
                                ui.label(subject.semester).style(
                                    "background:#f5f3ff; color:#6d28d9; padding:4px 10px; border-radius:999px; font-size:12px; font-weight:600;"
                                )
                                ui.label("Completed" if subject.is_completed else "Not completed").style(
                                    status_style(subject.is_completed)
                                )
                            ui.label(f"Tasks: {len(subject_tasks)}").classes("text-sm text-slate-600")
                            ui.label(f"Planned minutes: {sum(task.estimated_minutes for task in subject_tasks)}").classes("text-sm text-slate-600")

                ui.label("Completed Modules").classes("text-lg font-semibold text-slate-800")

                if not completed_subjects:
                    ui.label("No completed modules yet.").classes("text-slate-500")
                else:
                    for subject in completed_subjects:
                        with ui.card().style(card_style()):
                            ui.label(subject.name).classes("text-lg font-semibold text-slate-800")
                            ui.label(f"Semester: {subject.semester}").classes("text-sm text-slate-600")
                            ui.label(f"ECTS: {subject.ects}").classes("text-sm text-slate-600")

        def refresh_dashboard() -> None:
            refresh_credit_box()
            refresh_progress_box()
            refresh_urgent_task_list()
            refresh_week_overview()

        def handle_add_subject() -> None:
            if not subject_name_input.value:
                ui.notify("Please enter a subject name.")
                return

            try:
                ects = int(subject_ects_input.value or 0)
                if ects < 0:
                    ui.notify("ECTS must be 0 or greater.")
                    return
            except ValueError:
                ui.notify("Please enter a valid ECTS number.")
                return

            add_subject(
                subject_name_input.value,
                ects,
                subject_semester_select.value or "Semester 1",
                subject_moodle_link_input.value or "",
            )
            subject_name_input.value = ""
            subject_ects_input.value = ""
            subject_semester_select.value = "Semester 1"
            subject_moodle_link_input.value = ""
            refresh_subject_list()
            refresh_subject_options()
            refresh_dashboard()
            refresh_statistics_box()
            ui.notify("Subject added.")

        def handle_save_edited_subject() -> None:
            if edit_subject_state["id"] is None:
                ui.notify("No subject selected.")
                return

            if not edit_subject_name_input.value:
                ui.notify("Please enter a subject name.")
                return

            try:
                ects = int(edit_subject_ects_input.value or 0)
                if ects < 0:
                    ui.notify("ECTS must be 0 or greater.")
                    return
            except ValueError:
                ui.notify("Please enter a valid ECTS number.")
                return

            edit_subject(
                edit_subject_state["id"],
                edit_subject_name_input.value,
                ects,
                edit_subject_semester_select.value or "Semester 1",
                edit_subject_moodle_link_input.value or "",
                bool(edit_subject_completed_checkbox.value),
            )
            edit_subject_dialog.close()
            refresh_subject_list()
            refresh_subject_options()
            refresh_dashboard()
            refresh_statistics_box()
            ui.notify("Subject updated.")

        def handle_remove_subject(subject_id: int) -> None:
            tasks = get_tasks()
            linked_tasks = [task for task in tasks if task.subject_id == subject_id]

            if linked_tasks:
                ui.notify("You cannot delete a subject that still has tasks.")
                return

            remove_subject(subject_id)
            refresh_subject_list()
            refresh_subject_options()
            refresh_dashboard()
            refresh_statistics_box()
            ui.notify("Subject deleted.")

        def handle_add_task() -> None:
            if not task_subject_select.value:
                ui.notify("Please select a subject.")
                return

            if not task_title_input.value:
                ui.notify("Please enter a task title.")
                return

            try:
                deadline = build_optional_date(
                    deadline_day_select.value,
                    deadline_month_select.value,
                    deadline_year_select.value,
                    "deadline",
                )
            except ValueError:
                return

            try:
                planned_date = build_optional_date(
                    planned_day_select.value,
                    planned_month_select.value,
                    planned_year_select.value,
                    "planned date",
                )
            except ValueError:
                return

            try:
                estimated_minutes = int(estimated_minutes_input.value or 0)
                if estimated_minutes < 0:
                    ui.notify("Estimated minutes must be 0 or greater.")
                    return
            except ValueError:
                ui.notify("Please enter a valid number of minutes.")
                return

            add_task(
                task_title_input.value,
                deadline,
                planned_date,
                estimated_minutes,
                priority_select.value or "medium",
                task_notes_input.value or "",
                task_subject_select.value,
            )
            task_title_input.value = ""
            deadline_day_select.value = None
            deadline_month_select.value = None
            deadline_year_select.value = None
            planned_day_select.value = None
            planned_month_select.value = None
            planned_year_select.value = None
            estimated_minutes_input.value = ""
            priority_select.value = "medium"
            task_notes_input.value = ""
            task_subject_select.value = None
            refresh_task_list()
            refresh_dashboard()
            refresh_statistics_box()
            ui.notify("Task added.")

        def handle_complete_task(task_id: int) -> None:
            complete_task(task_id)
            refresh_task_list()
            refresh_dashboard()
            refresh_statistics_box()
            ui.notify("Task completed.")

        def handle_export_subjects() -> None:
            path = export_subjects_csv()
            ui.notify(f"Subjects exported to: {path}")

        def handle_export_tasks() -> None:
            path = export_tasks_csv()
            ui.notify(f"Tasks exported to: {path}")

        add_subject_button.on("click", lambda: handle_add_subject())
        add_task_button.on("click", lambda: handle_add_task())
        export_subjects_button.on("click", lambda: handle_export_subjects())
        export_tasks_button.on("click", lambda: handle_export_tasks())
        cancel_edit_subject_button.on("click", lambda: edit_subject_dialog.close())
        save_edit_subject_button.on("click", lambda: handle_save_edited_subject())

        refresh_subject_options()
        refresh_subject_list()
        refresh_task_list()
        refresh_dashboard()
        refresh_statistics_box()
