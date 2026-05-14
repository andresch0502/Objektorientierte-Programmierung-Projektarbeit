from nicegui import ui

from study_planner.ui.controllers import get_app_title


def show_home_page() -> None:
    ui.label(get_app_title())
