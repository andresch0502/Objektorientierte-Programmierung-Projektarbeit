from nicegui import ui

from study_planner.ui.controllers import (
    add_subject,
    add_task,
    get_app_title,
    get_subjects,
    get_tasks,
)


def show_home_page() -> None:
    ui.label(get_app_title())

    ui.label("Subjects")

    name_input = ui.input("Subject name")
    description_input = ui.input("Description")

    subject_list = ui.column()

    task_title_input = ui.input("Task title")
    task_description_input = ui.input("Task description")
    subject_select = ui.select(options={}, label="Subject")

    task_list = ui.column()

    def refresh_subject_list() -> None:
        subject_list.clear()
        with subject_list:
            subjects = get_subjects()
            for subject in subjects:
                ui.label(subject.name)

    def refresh_subject_options() -> None:
        subjects = get_subjects()
        subject_select.options = {
            subject.id: subject.name
            for subject in subjects
            if subject.id is not None
        }
        subject_select.update()

    def refresh_task_list() -> None:
        task_list.clear()
        with task_list:
            tasks = get_tasks()
            for task in tasks:
                ui.label(task.title)

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

        add_task(
            task_title_input.value,
            task_description_input.value or "",
            subject_select.value,
        )
        task_title_input.value = ""
        task_description_input.value = ""
        subject_select.value = None
        refresh_task_list()

    ui.button("Add subject", on_click=handle_add_subject)

    refresh_subject_list()
    refresh_subject_options()

    ui.separator()
    ui.label("Tasks")

    ui.button("Add task", on_click=handle_add_task)

    refresh_task_list()
