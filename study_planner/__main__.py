from nicegui import ui

from study_planner.application import setup_app


def main() -> None:
    setup_app()
    ui.run(
        title="StudyPlanner",
        storage_secret="studyplanner-secret-key",
        reload=False,
    )


if __name__ in {"__main__", "__mp_main__"}:
    main()
