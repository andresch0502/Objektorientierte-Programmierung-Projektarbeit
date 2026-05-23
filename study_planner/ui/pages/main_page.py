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
from study_planner.ui.pages.auth_view import build_app_header, build_login_view
from study_planner.ui.pages.dashboard_section import build_dashboard_tab
from study_planner.ui.pages.page_actions import (
    handle_add_subject,
    handle_add_task,
    handle_complete_task,
    handle_export_subjects,
    handle_export_tasks,
    handle_login,
    handle_logout,
    handle_remove_subject,
    handle_save_edited_subject,
)
from study_planner.ui.pages.page_helpers import build_optional_date
from study_planner.ui.pages.page_refresh import (
    refresh_dashboard,
    refresh_statistics,
    refresh_subject_options,
    refresh_subjects,
    refresh_tasks,
)
from study_planner.ui.pages.statistics_section import build_statistics_tab
from study_planner.ui.pages.subjects_section import (
    build_edit_subject_dialog,
    build_subjects_tab,
)
from study_planner.ui.pages.tasks_section import build_tasks_tab


def show_home_page() -> None:
    ui.query("body").style(
        "background: linear-gradient(180deg, #f8fafc 0%, #eef2ff 45%, #f8fafc 100%); "
        "min-height: 100vh;"
    )

    if not is_logged_in():
        login_components = build_login_view(
            lambda: handle_login(
                login_components["username_input"],
                login_components["password_input"],
                login,
            )
        )
        return

    def on_logout() -> None:
        handle_logout(logout)

    with ui.column().style(
        "max-width: 1280px; margin: 0 auto; padding: 28px; width: 100%; gap: 22px;"
    ):
        build_app_header(
            get_app_title(),
            get_logged_in_username(),
            on_logout,
        )

        edit_subject_state = {"id": None}

        with ui.tabs().classes("w-full") as tabs:
            dashboard_tab = ui.tab("🏠 Dashboard")
            subjects_tab = ui.tab("📚 Subjects")
            tasks_tab = ui.tab("📝 Tasks")
            statistics_tab = ui.tab("📊 Statistics")

        with ui.tab_panels(tabs, value=dashboard_tab).classes("w-full"):
            dashboard_components = build_dashboard_tab(
                dashboard_tab,
                lambda: do_refresh_dashboard(),
            )
            subjects_components = build_subjects_tab(
                subjects_tab,
                lambda: on_add_subject(),
            )
            tasks_components = build_tasks_tab(
                tasks_tab,
                lambda: {},
                lambda: on_add_task(),
            )
            statistics_components = build_statistics_tab(
                statistics_tab,
                lambda: do_refresh_statistics(),
                lambda: on_export_subjects(),
                lambda: on_export_tasks(),
            )

        dialog_components = build_edit_subject_dialog(
            lambda: on_save_edited_subject(),
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

        def do_refresh_subject_options() -> None:
            refresh_subject_options(task_subject_select, get_subjects)

        def do_refresh_subjects() -> None:
            refresh_subjects(
                subject_list,
                get_subjects,
                open_edit_subject_dialog,
                on_remove_subject,
            )

        def do_refresh_tasks() -> None:
            refresh_tasks(
                task_list,
                get_tasks,
                get_subjects,
                on_complete_task,
            )

        def do_refresh_dashboard() -> None:
            refresh_dashboard(
                dashboard_semester_select,
                credit_box,
                progress_box,
                urgent_task_list,
                week_overview_box,
                get_subjects,
                get_tasks,
                get_credit_summary,
            )

        def do_refresh_statistics() -> None:
            refresh_statistics(
                statistics_semester_select,
                statistics_box,
                get_subjects,
                get_tasks,
                get_tasks_per_subject,
                get_priority_distribution,
                get_semester_statistics,
                get_completed_subjects,
            )

        def on_add_subject() -> None:
            handle_add_subject(
                subject_name_input,
                subject_ects_input,
                subject_semester_select,
                subject_moodle_link_input,
                add_subject,
                do_refresh_subjects,
                do_refresh_subject_options,
                do_refresh_dashboard,
                do_refresh_statistics,
            )

        def on_save_edited_subject() -> None:
            handle_save_edited_subject(
                edit_subject_state,
                edit_subject_name_input,
                edit_subject_ects_input,
                edit_subject_semester_select,
                edit_subject_moodle_link_input,
                edit_subject_completed_checkbox,
                edit_subject_dialog,
                edit_subject,
                do_refresh_subjects,
                do_refresh_subject_options,
                do_refresh_dashboard,
                do_refresh_statistics,
            )

        def on_remove_subject(subject_id: int) -> None:
            handle_remove_subject(
                subject_id,
                get_tasks,
                remove_subject,
                do_refresh_subjects,
                do_refresh_subject_options,
                do_refresh_dashboard,
                do_refresh_statistics,
            )

        def on_add_task() -> None:
            handle_add_task(
                task_subject_select,
                task_title_input,
                deadline_day_select,
                deadline_month_select,
                deadline_year_select,
                planned_day_select,
                planned_month_select,
                planned_year_select,
                estimated_minutes_input,
                priority_select,
                task_notes_input,
                build_optional_date,
                add_task,
                do_refresh_tasks,
                do_refresh_dashboard,
                do_refresh_statistics,
            )

        def on_complete_task(task_id: int) -> None:
            handle_complete_task(
                task_id,
                complete_task,
                do_refresh_tasks,
                do_refresh_dashboard,
                do_refresh_statistics,
            )

        def on_export_subjects() -> None:
            handle_export_subjects(export_subjects_csv)

        def on_export_tasks() -> None:
            handle_export_tasks(export_tasks_csv)

        do_refresh_subject_options()
        do_refresh_subjects()
        do_refresh_tasks()
        do_refresh_dashboard()
        do_refresh_statistics()
