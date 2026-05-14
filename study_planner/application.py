from nicegui import ui

from study_planner.data_access.db import Database
import study_planner.domain.models  # ensures SQLModel tables are registered
from study_planner.ui.pages import show_home_page


database = Database()


def start() -> None:
    database.init_schema()
    show_home_page()
    ui.run()
