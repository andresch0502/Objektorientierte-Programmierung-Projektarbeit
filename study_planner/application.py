from nicegui import ui

from study_planner.data_access.db import Database
import study_planner.domain.models  # ensures SQLModel tables are registered


database = Database()


def start() -> None:
    database.init_schema()
    ui.label("StudyPlanner")
    ui.run()
