from datetime import date, timedelta

from nicegui import ui

from study_planner.ui.pages.shared import (
    SEMESTER_OPTIONS,
    card_style,
    info_card,
    priority_style,
    section_title,
)


def build_dashboard_tab(dashboard_tab, on_semester_change):
    with ui.tab_panel(dashboard_tab):
        with ui.card().style(card_style()):
            section_title("Semester View", "Filter the dashboard by semester.")
            dashboard_semester_select = ui.select(
                options=SEMESTER_OPTIONS,
                label="Semester filter",
                value="All semesters",
                on_change=lambda _: on_semester_change(),
            ).classes("w-full max-w-xs")

        credit_box = ui.column().classes("w-full")
        progress_box = ui.column().classes("w-full")
        urgent_task_list = ui.column().classes("w-full")
        week_overview_box = ui.column().classes("w-full")

    return {
        "dashboard_semester_select": dashboard_semester_select,
        "credit_box": credit_box,
        "progress_box": progress_box,
        "urgent_task_list": urgent_task_list,
        "week_overview_box": week_overview_box,
    }


def refresh_credit_box(credit_box, selected_semester: str, credits: dict[str, int]) -> None:
    credit_box.clear()
    with credit_box:
        section_title("🎓 Credits Overview", f"Showing credits for: {selected_semester}")

        with ui.row().classes("w-full").style("gap: 14px; flex-wrap: wrap;"):
            info_card(
                "Planned Credits",
                str(credits["planned"]),
                "linear-gradient(135deg, #dbeafe 0%, #eff6ff 100%)",
                "#1e3a8a",
            )
            info_card(
                "Completed Credits",
                str(credits["completed"]),
                "linear-gradient(135deg, #dcfce7 0%, #f0fdf4 100%)",
                "#166534",
            )
            info_card(
                "Open Credits",
                str(credits["open"]),
                "linear-gradient(135deg, #fee2e2 0%, #fff1f2 100%)",
                "#9f1239",
            )


def refresh_progress_box(progress_box, selected_semester: str, tasks: list) -> None:
    progress_box.clear()
    with progress_box:
        section_title("📈 Progress", f"Task status for: {selected_semester}")

        total = len(tasks)
        completed = len([task for task in tasks if task.is_completed])
        open_tasks = total - completed

        with ui.row().classes("w-full").style("gap: 14px; flex-wrap: wrap;"):
            info_card(
                "Filtered tasks",
                str(total),
                "linear-gradient(135deg, #e0f2fe 0%, #f8fafc 100%)",
                "#0f172a",
            )
            info_card(
                "Completed",
                str(completed),
                "linear-gradient(135deg, #dcfce7 0%, #f0fdf4 100%)",
                "#166534",
            )
            info_card(
                "Open",
                str(open_tasks),
                "linear-gradient(135deg, #fef3c7 0%, #fffbeb 100%)",
                "#92400e",
            )


def refresh_urgent_task_list(
    urgent_task_list,
    selected_semester: str,
    tasks: list,
    subject_names: dict[int, str],
) -> None:
    urgent_task_list.clear()
    with urgent_task_list:
        section_title("⚠️ Urgent Tasks", f"Urgent tasks for: {selected_semester}")

        urgent_tasks = [
            task
            for task in tasks
            if not task.is_completed and task.deadline is not None
        ]
        urgent_tasks = sorted(urgent_tasks, key=lambda task: task.deadline)[:3]

        if not urgent_tasks:
            with ui.card().style(card_style()):
                ui.label("No urgent tasks at the moment.").classes("text-slate-500")
            return

        with ui.row().classes("w-full").style("gap: 14px; flex-wrap: wrap;"):
            for task in urgent_tasks:
                with ui.card().style(
                    "flex: 1; min-width: 260px; border-radius: 20px; padding: 16px; "
                    "box-shadow: 0 10px 28px rgba(15, 23, 42, 0.08); background: #ffffff;"
                ):
                    ui.label(task.title).classes("text-lg font-semibold text-slate-800")
                    if task.subject_id in subject_names:
                        ui.label(f"Subject: {subject_names[task.subject_id]}").classes("text-sm text-slate-600")

                    with ui.row().classes("items-center").style("gap: 8px; margin-top: 8px; flex-wrap: wrap;"):
                        ui.label(task.priority.capitalize()).style(priority_style(task.priority))
                        if task.deadline:
                            ui.label(f"Deadline: {task.deadline}").style(
                                "background:#fee2e2;color:#b91c1c;padding:4px 10px;"
                                "border-radius:999px;font-size:12px;font-weight:600;"
                            )

                    if task.estimated_minutes:
                        ui.label(f"Planned effort: {task.estimated_minutes} minutes").classes("text-sm text-slate-600")
                    if task.notes:
                        ui.label(task.notes).classes("text-sm text-slate-500")


def refresh_week_overview(
    week_overview_box,
    selected_semester: str,
    tasks: list,
    subject_names: dict[int, str],
) -> None:
    week_overview_box.clear()
    with week_overview_box:
        section_title("🗓️ Weekly Calendar", f"Planned tasks for the next 7 days ({selected_semester})")

        start_day = date.today()

        with ui.element("div").style(
            "display: grid; grid-template-columns: repeat(7, minmax(150px, 1fr)); "
            "gap: 12px; width: 100%;"
        ):
            for offset in range(7):
                current_day = start_day + timedelta(days=offset)
                day_tasks = [task for task in tasks if task.planned_date == current_day]

                with ui.card().style(
                    "min-height: 260px; width: 100%; border-radius: 18px; padding: 14px; "
                    "box-shadow: 0 10px 22px rgba(15, 23, 42, 0.08); background: #ffffff;"
                ):
                    ui.label(current_day.strftime("%a")).classes("text-sm text-slate-500")
                    ui.label(current_day.strftime("%d.%m.%Y")).classes("font-semibold text-slate-800")

                    if not day_tasks:
                        ui.label("No tasks").classes("text-sm text-slate-400")
                        continue

                    for task in day_tasks:
                        subject_text = subject_names.get(task.subject_id, "No subject")

                        with ui.card().style(
                            "width: 100%; margin-top: 8px; border-radius: 14px; "
                            "padding: 10px; background: #f8fafc; box-shadow: none;"
                        ):
                            ui.label(task.title).classes("text-sm font-medium text-slate-800")
                            ui.label(subject_text).classes("text-xs text-slate-600")
                            ui.label(task.priority.capitalize()).style(priority_style(task.priority))

                            if task.estimated_minutes:
                                ui.label(f"{task.estimated_minutes} min").classes("text-xs text-slate-600")

                            if task.deadline:
                                ui.label(f"Due: {task.deadline}").classes("text-xs text-red-600")
