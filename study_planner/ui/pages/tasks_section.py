from nicegui import ui

from study_planner.ui.pages.shared import card_style, priority_style, section_title, status_style


def build_tasks_tab(tasks_tab, subject_options_provider, on_add_task):
    with ui.tab_panel(tasks_tab):
        with ui.card().style(card_style()):
            section_title(
                "📝 Add Task",
                "Mandatory: Subject, Task title, Priority. Optional: deadline, planned date, estimated minutes, notes.",
            )

            task_subject_select = ui.select(
                options=subject_options_provider(),
                label="Subject *",
            ).classes("w-full")
            task_title_input = ui.input("Task title *").classes("w-full")

            priority_select = ui.select(
                options={
                    "high": "High",
                    "medium": "Medium",
                    "low": "Low",
                },
                label="Priority *",
                value="medium",
            ).classes("w-full")

            ui.label("Deadline (optional)").classes("text-sm text-slate-600")
            with ui.row().classes("w-full").style("gap: 12px; flex-wrap: wrap;"):
                deadline_day_select = ui.select(
                    options=[str(day) for day in range(1, 32)],
                    label="Day",
                ).classes("w-full")
                deadline_month_select = ui.select(
                    options=[str(month) for month in range(1, 13)],
                    label="Month",
                ).classes("w-full")
                deadline_year_select = ui.select(
                    options=[str(year) for year in range(2025, 2036)],
                    label="Year",
                ).classes("w-full")

            ui.label("Planned date (optional)").classes("text-sm text-slate-600")
            with ui.row().classes("w-full").style("gap: 12px; flex-wrap: wrap;"):
                planned_day_select = ui.select(
                    options=[str(day) for day in range(1, 32)],
                    label="Day",
                ).classes("w-full")
                planned_month_select = ui.select(
                    options=[str(month) for month in range(1, 13)],
                    label="Month",
                ).classes("w-full")
                planned_year_select = ui.select(
                    options=[str(year) for year in range(2025, 2036)],
                    label="Year",
                ).classes("w-full")

            estimated_minutes_input = ui.input("Estimated minutes (optional)").classes("w-full")
            task_notes_input = ui.textarea("Notes (optional)").classes("w-full")
            add_task_button = ui.button("Add task", on_click=on_add_task).classes("w-full").props("color=primary")

        with ui.card().style(card_style()):
            section_title("✅ Task Overview", "All planned and completed tasks.")
            task_list = ui.column().classes("w-full")

    return {
        "task_subject_select": task_subject_select,
        "task_title_input": task_title_input,
        "priority_select": priority_select,
        "deadline_day_select": deadline_day_select,
        "deadline_month_select": deadline_month_select,
        "deadline_year_select": deadline_year_select,
        "planned_day_select": planned_day_select,
        "planned_month_select": planned_month_select,
        "planned_year_select": planned_year_select,
        "estimated_minutes_input": estimated_minutes_input,
        "task_notes_input": task_notes_input,
        "add_task_button": add_task_button,
        "task_list": task_list,
    }


def refresh_task_subject_options(task_subject_select, options: dict[int, str]) -> None:
    task_subject_select.options = options
    task_subject_select.update()


def refresh_task_list(task_list, tasks, subject_names: dict[int, str], handle_complete_task) -> None:
    task_list.clear()
    with task_list:
        if not tasks:
            ui.label("No tasks added yet.").classes("text-slate-500")
            return

        for task in tasks:
            with ui.card().style(card_style()):
                with ui.row().style(
                    "width: 100%; justify-content: space-between; align-items: flex-start; gap: 12px;"
                ):
                    with ui.column().classes("gap-2"):
                        title_prefix = "✅ " if task.is_completed else ""
                        ui.label(f"{title_prefix}{task.title}").classes("text-lg font-semibold text-slate-800")

                        with ui.row().classes("items-center").style("gap: 8px; flex-wrap: wrap;"):
                            if task.subject_id in subject_names:
                                ui.label(subject_names[task.subject_id]).style(
                                    "background:#eff6ff; color:#1d4ed8; padding:4px 10px; border-radius:999px; "
                                    "font-size:12px; font-weight:600;"
                                )

                            ui.label(task.priority.capitalize()).style(priority_style(task.priority))
                            ui.label("Completed" if task.is_completed else "Open").style(
                                status_style(task.is_completed)
                            )

                        if task.deadline:
                            ui.label(f"Deadline: {task.deadline}").classes("text-sm text-slate-600")

                        if task.planned_date:
                            ui.label(f"Planned date: {task.planned_date}").classes("text-sm text-slate-600")

                        if task.estimated_minutes:
                            ui.label(
                                f"Estimated time: {task.estimated_minutes} minutes"
                            ).classes("text-sm text-slate-600")

                        if task.notes:
                            ui.label(task.notes).classes("text-sm text-slate-500")

                    if not task.is_completed and task.id is not None:
                        ui.button(
                            "Complete",
                            on_click=lambda task_id=task.id: handle_complete_task(task_id),
                        ).props("color=positive")
