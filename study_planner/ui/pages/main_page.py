from datetime import date

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
from study_planner.ui.pages.dashboard_section import (
    build_dashboard_tab,
    refresh_credit_box,
    refresh_progress_box,
    refresh_urgent_task_list,
    refresh_week_overview,
)
from study_planner.ui.pages.statistics_section import (
    build_statistics_tab,
    refresh_statistics_box,
)
from study_planner.ui.pages.subjects_section import (
    build_edit_subject_dialog,
    build_subjects_tab,
    refresh_subject_list,
)
from study_planner.ui.pages.tasks_section import (
    build_tasks_tab,
    refresh_task_list,
    refresh_task_subject_options,
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

        with ui.tabs().classes("w-full") as tabs:
            dashboard_tab = ui.tab("🏠 Dashboard")
            subjects_tab = ui.tab("📚 Subjects")
            tasks_tab = ui.tab("📝 Tasks")
            statistics_tab = ui.tab("📊 Statistics")

        with ui.tab_panels(tabs, value=dashboard_tab).classes("w-full"):
            dashboard_components = build_dashboard_tab(
                dashboard_tab,
                lambda: refresh_dashboard(),
            )
            subjects_components = build_subjects_tab(
                subjects_tab,
                lambda: handle_add_subject(),
            )
            tasks_components = build_tasks_tab(
                tasks_tab,
                lambda: {},
                lambda: handle_add_task(),
            )
            statistics_components = build_statistics_tab(
                statistics_tab,
                lambda: refresh_statistics(),
                lambda: handle_export_subjects(),
                lambda: handle_export_tasks(),
            )

        dialog_components = build_edit_subject_dialog(
            lambda: handle_save_edited_subject(),
        )

        dashboard_semester_select = dashboard_components["dashboard_semester_select"]
        credit_box = dashboard_components["credit_box"]
        progress_box = dashboard_components["progress_box"]
        urgent_task_list = dashboard_components["urgent_task_list"]
        week_overview_box = dashboard_components["week_overview_box"]

        subject_name_input = subjects_components["subject_name_input"]
        subject_ects_input = subjects_components["subject_ects_input"]
        subject_semester_select = subjects_components["subject_semester_select"]
        subject_moodle_link_input = subjects_components["subject_moodle_link_input"]
        subject_list = subjects_components["subject_list"]

        task_subject_select = tasks_components["task_subject_select"]
        task_title_input = tasks_components["task_title_input"]
        priority_select = tasks_components["priority_select"]
        deadline_day_select = tasks_components["deadline_day_select"]
        deadline_month_select = tasks_components["deadline_month_select"]
        deadline_year_select = tasks_components["deadline_year_select"]
        planned_day_select = tasks_components["planned_day_select"]
        planned_month_select = tasks_components["planned_month_select"]
        planned_year_select = tasks_components["planned_year_select"]
        estimated_minutes_input = tasks_components["estimated_minutes_input"]
        task_notes_input = tasks_components["task_notes_input"]
        task_list = tasks_components["task_list"]

        statistics_semester_select = statistics_components["statistics_semester_select"]
        statistics_box = statistics_components["statistics_box"]

        edit_subject_dialog = dialog_components["edit_subject_dialog"]
        edit_subject_name_input = dialog_components["edit_subject_name_input"]
        edit_subject_ects_input = dialog_components["edit_subject_ects_input"]
        edit_subject_semester_select = dialog_components["edit_subject_semester_select"]
        edit_subject_moodle_link_input = dialog_components["edit_subject_moodle_link_input"]
        edit_subject_completed_checkbox = dialog_components["edit_subject_completed_checkbox"]

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

        def refresh_subject_options() -> None:
            refresh_task_subject_options(task_subject_select, get_subject_name_map())

        def refresh_subjects() -> None:
            refresh_subject_list(
                subject_list,
                get_subjects(),
                open_edit_subject_dialog,
                handle_remove_subject,
            )

        def refresh_tasks() -> None:
            refresh_task_list(
                task_list,
                get_tasks(),
                get_subject_name_map(),
                handle_complete_task,
            )

        def refresh_dashboard() -> None:
            selected_semester = dashboard_semester_select.value or "All semesters"
            filtered_tasks = get_filtered_dashboard_tasks()
            subject_names = get_subject_name_map()

            refresh_credit_box(
                credit_box,
                selected_semester,
                get_credit_summary(selected_semester),
            )
            refresh_progress_box(
                progress_box,
                selected_semester,
                filtered_tasks,
            )
            refresh_urgent_task_list(
                urgent_task_list,
                selected_semester,
                filtered_tasks,
                subject_names,
            )
            refresh_week_overview(
                week_overview_box,
                selected_semester,
                filtered_tasks,
                subject_names,
            )

        def refresh_statistics() -> None:
            selected_semester = statistics_semester_select.value or "All semesters"
            refresh_statistics_box(
                statistics_box,
                selected_semester,
                get_statistics_tasks(),
                get_statistics_subjects(),
                get_tasks_per_subject(selected_semester),
                get_priority_distribution(selected_semester),
                get_semester_statistics(),
                get_completed_subjects(selected_semester),
            )

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

            refresh_subjects()
            refresh_subject_options()
            refresh_dashboard()
            refresh_statistics()
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
            refresh_subjects()
            refresh_subject_options()
            refresh_dashboard()
            refresh_statistics()
            ui.notify("Subject updated.")

        def handle_remove_subject(subject_id: int) -> None:
            tasks = get_tasks()
            linked_tasks = [task for task in tasks if task.subject_id == subject_id]

            if linked_tasks:
                ui.notify("You cannot delete a subject that still has tasks.")
                return

            remove_subject(subject_id)
            refresh_subjects()
            refresh_subject_options()
            refresh_dashboard()
            refresh_statistics()
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

            refresh_tasks()
            refresh_dashboard()
            refresh_statistics()
            ui.notify("Task added.")

        def handle_complete_task(task_id: int) -> None:
            complete_task(task_id)
            refresh_tasks()
            refresh_dashboard()
            refresh_statistics()
            ui.notify("Task completed.")

        def handle_export_subjects() -> None:
            path = export_subjects_csv()
            ui.notify(f"Subjects exported to: {path}")

        def handle_export_tasks() -> None:
            path = export_tasks_csv()
            ui.notify(f"Tasks exported to: {path}")

        refresh_subject_options()
        refresh_subjects()
        refresh_tasks()
        refresh_dashboard()
        refresh_statistics()
