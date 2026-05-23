from nicegui import ui


def handle_login(username_input, password_input, login_func) -> None:
    username = username_input.value or ""
    password = password_input.value or ""

    if login_func(username, password):
        ui.notify("Login successful.")
        ui.navigate.reload()
    else:
        ui.notify("Invalid username or password.", color="negative")


def handle_logout(logout_func) -> None:
    logout_func()
    ui.notify("Logged out.")
    ui.navigate.reload()


def handle_add_subject(
    subject_name_input,
    subject_ects_input,
    subject_semester_select,
    subject_moodle_link_input,
    add_subject_func,
    refresh_subjects_func,
    refresh_subject_options_func,
    refresh_dashboard_func,
    refresh_statistics_func,
) -> None:
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

    add_subject_func(
        subject_name_input.value,
        ects,
        subject_semester_select.value or "Semester 1",
        subject_moodle_link_input.value or "",
    )

    subject_name_input.value = ""
    subject_ects_input.value = ""
    subject_semester_select.value = "Semester 1"
    subject_moodle_link_input.value = ""

    refresh_subjects_func()
    refresh_subject_options_func()
    refresh_dashboard_func()
    refresh_statistics_func()
    ui.notify("Subject added.")


def handle_save_edited_subject(
    edit_subject_state,
    edit_subject_name_input,
    edit_subject_ects_input,
    edit_subject_semester_select,
    edit_subject_moodle_link_input,
    edit_subject_completed_checkbox,
    edit_subject_dialog,
    edit_subject_func,
    refresh_subjects_func,
    refresh_subject_options_func,
    refresh_dashboard_func,
    refresh_statistics_func,
) -> None:
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

    edit_subject_func(
        edit_subject_state["id"],
        edit_subject_name_input.value,
        ects,
        edit_subject_semester_select.value or "Semester 1",
        edit_subject_moodle_link_input.value or "",
        bool(edit_subject_completed_checkbox.value),
    )

    edit_subject_dialog.close()
    refresh_subjects_func()
    refresh_subject_options_func()
    refresh_dashboard_func()
    refresh_statistics_func()
    ui.notify("Subject updated.")


def handle_remove_subject(
    subject_id: int,
    get_tasks_func,
    remove_subject_func,
    refresh_subjects_func,
    refresh_subject_options_func,
    refresh_dashboard_func,
    refresh_statistics_func,
) -> None:
    tasks = get_tasks_func()
    linked_tasks = [task for task in tasks if task.subject_id == subject_id]

    if linked_tasks:
        ui.notify("You cannot delete a subject that still has tasks.")
        return

    remove_subject_func(subject_id)
    refresh_subjects_func()
    refresh_subject_options_func()
    refresh_dashboard_func()
    refresh_statistics_func()
    ui.notify("Subject deleted.")


def handle_add_task(
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
    build_optional_date_func,
    add_task_func,
    refresh_tasks_func,
    refresh_dashboard_func,
    refresh_statistics_func,
) -> None:
    if not task_subject_select.value:
        ui.notify("Please select a subject.")
        return

    if not task_title_input.value:
        ui.notify("Please enter a task title.")
        return

    try:
        deadline = build_optional_date_func(
            deadline_day_select.value,
            deadline_month_select.value,
            deadline_year_select.value,
        )
    except ValueError:
        ui.notify("Please select a complete and valid deadline.")
        return

    try:
        planned_date = build_optional_date_func(
            planned_day_select.value,
            planned_month_select.value,
            planned_year_select.value,
        )
    except ValueError:
        ui.notify("Please select a complete and valid planned date.")
        return

    try:
        estimated_minutes = int(estimated_minutes_input.value or 0)
        if estimated_minutes < 0:
            ui.notify("Estimated minutes must be 0 or greater.")
            return
    except ValueError:
        ui.notify("Please enter a valid number of minutes.")
        return

    add_task_func(
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

    refresh_tasks_func()
    refresh_dashboard_func()
    refresh_statistics_func()
    ui.notify("Task added.")


def handle_complete_task(
    task_id: int,
    complete_task_func,
    refresh_tasks_func,
    refresh_dashboard_func,
    refresh_statistics_func,
) -> None:
    complete_task_func(task_id)
    refresh_tasks_func()
    refresh_dashboard_func()
    refresh_statistics_func()
    ui.notify("Task completed.")


def handle_export_subjects(export_subjects_csv_func) -> None:
    path = export_subjects_csv_func()
    ui.notify(f"Subjects exported to: {path}")


def handle_export_tasks(export_tasks_csv_func) -> None:
    path = export_tasks_csv_func()
    ui.notify(f"Tasks exported to: {path}")
