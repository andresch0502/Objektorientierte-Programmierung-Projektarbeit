from nicegui import ui

from study_planner.application import setup_app


setup_app()
ui.run(
    title="StudyPlanner",
    storage_secret="studyplanner-secret-key",
)
