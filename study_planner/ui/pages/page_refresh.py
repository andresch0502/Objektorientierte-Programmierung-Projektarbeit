from study_planner.ui.pages.dashboard_section import (
    refresh_credit_box,
    refresh_progress_box,
    refresh_urgent_task_list,
    refresh_week_overview,
)
from study_planner.ui.pages.page_helpers import (
    get_filtered_dashboard_tasks,
    get_statistics_subjects,
    get_statistics_tasks,
    get_subject_name_map,
)
from study_planner.ui.pages.statistics_section import refresh_statistics_box
from study_planner.ui.pages.subjects_section import refresh_subject_list
from study_planner.ui.pages.tasks_section import (
    refresh_task_list,
    refresh_task_subject_options,
)


def refresh_subject_options(task_subject_select, get_subjects_func) -> None:
    refresh_task_subject_options(
        task_subject_select,
        get_subject_name_map(get_subjects_func()),
    )


def refresh_subjects(subject_list, get_subjects_func, open_edit_subject_dialog, handle_remove_subject) -> None:
    refresh_subject_list(
        subject_list,
        get_subjects_func(),
        open_edit_subject_dialog,
        handle_remove_subject,
    )


def refresh_tasks(task_list, get_tasks_func, get_subjects_func, handle_complete_task) -> None:
    refresh_task_list(
        task_list,
        get_tasks_func(),
        get_subject_name_map(get_subjects_func()),
        handle_complete_task,
    )


def refresh_dashboard(
    dashboard_semester_select,
    credit_box,
    progress_box,
    urgent_task_list,
    week_overview_box,
    get_subjects_func,
    get_tasks_func,
    get_credit_summary_func,
) -> None:
    selected_semester = dashboard_semester_select.value or "All semesters"
    subjects = get_subjects_func()
    tasks = get_tasks_func()
    filtered_tasks = get_filtered_dashboard_tasks(tasks, subjects, selected_semester)
    subject_names = get_subject_name_map(subjects)

    refresh_credit_box(
        credit_box,
        selected_semester,
        get_credit_summary_func(selected_semester),
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


def refresh_statistics(
    statistics_semester_select,
    statistics_box,
    get_subjects_func,
    get_tasks_func,
    get_tasks_per_subject_func,
    get_priority_distribution_func,
    get_semester_statistics_func,
    get_completed_subjects_func,
) -> None:
    selected_semester = statistics_semester_select.value or "All semesters"
    subjects = get_subjects_func()
    tasks = get_tasks_func()

    refresh_statistics_box(
        statistics_box,
        selected_semester,
        get_statistics_tasks(tasks, subjects, selected_semester),
        get_statistics_subjects(subjects, selected_semester),
        get_tasks_per_subject_func(selected_semester),
        get_priority_distribution_func(selected_semester),
        get_semester_statistics_func(),
        get_completed_subjects_func(selected_semester),
    )
