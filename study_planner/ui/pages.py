from nicegui import ui

from study_planner.ui.controllers import get_app_title, get_subjects


def show_home_page() -> None:
    ui.label(get_app_title())

    ui.label("Subjects")

    subjects = get_subjects()
    for subject in subjects:
        ui.label(subject.name)
