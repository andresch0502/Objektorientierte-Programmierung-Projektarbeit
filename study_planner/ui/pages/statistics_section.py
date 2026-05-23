from nicegui import ui

from study_planner.ui.pages.shared import SEMESTER_OPTIONS, card_style, info_card, section_title, status_style


def build_statistics_tab(statistics_tab, on_statistics_change, on_export_subjects, on_export_tasks):
    with ui.tab_panel(statistics_tab):
        with ui.card().style(card_style()):
            section_title("📤 Export", "Export subjects and tasks as CSV files for Excel.")
            export_subjects_button = ui.button(
                "Export Subjects CSV",
                on_click=on_export_subjects,
            ).classes("w-full").props("color=primary")
            export_tasks_button = ui.button(
                "Export Tasks CSV",
                on_click=on_export_tasks,
            ).classes("w-full").props("color=primary")

        with ui.card().style(card_style()):
            section_title("🧮 Statistics Filter", "Limit charts and summary cards to a single semester.")
            statistics_semester_select = ui.select(
                options=SEMESTER_OPTIONS,
                label="Semester filter",
                value="All semesters",
                on_change=lambda _: on_statistics_change(),
            ).classes("w-full max-w-xs")

        statistics_box = ui.column().classes("w-full")

    return {
        "export_subjects_button": export_subjects_button,
        "export_tasks_button": export_tasks_button,
        "statistics_semester_select": statistics_semester_select,
        "statistics_box": statistics_box,
    }


def refresh_statistics_box(
    statistics_box,
    selected_semester: str,
    tasks,
    subjects,
    tasks_per_subject,
    priority_distribution,
    semester_statistics,
    completed_subjects,
) -> None:
    statistics_box.clear()
    with statistics_box:
        section_title("📊 Statistics", f"Showing statistics for: {selected_semester}")

        if not tasks and not subjects:
            with ui.card().style(card_style()):
                ui.label("No statistics available yet.").classes("text-slate-500")
            return

        with ui.row().classes("w-full").style("gap: 14px; flex-wrap: wrap;"):
            info_card(
                "Total Subjects",
                str(len(subjects)),
                "linear-gradient(135deg, #ede9fe 0%, #f5f3ff 100%)",
                "#5b21b6",
            )
            info_card(
                "Total Tasks",
                str(len(tasks)),
                "linear-gradient(135deg, #e0f2fe 0%, #f8fafc 100%)",
                "#0f172a",
            )
            info_card(
                "Planned Minutes",
                str(sum(task.estimated_minutes for task in tasks)),
                "linear-gradient(135deg, #fef3c7 0%, #fffbeb 100%)",
                "#92400e",
            )

        with ui.row().classes("w-full").style("gap: 18px; flex-wrap: wrap;"):
            with ui.card().style(
                "flex: 1; min-width: 320px; border-radius: 20px; padding: 18px; "
                "box-shadow: 0 10px 28px rgba(15, 23, 42, 0.08);"
            ):
                ui.label("Tasks per Subject").classes("text-lg font-semibold text-slate-800")
                ui.echart({
                    "xAxis": {
                        "type": "category",
                        "data": [item["subject"] for item in tasks_per_subject],
                    },
                    "yAxis": {"type": "value"},
                    "series": [
                        {
                            "type": "bar",
                            "data": [item["count"] for item in tasks_per_subject],
                        }
                    ],
                    "tooltip": {},
                }).style("height: 350px; width: 100%;")

            with ui.card().style(
                "flex: 1; min-width: 320px; border-radius: 20px; padding: 18px; "
                "box-shadow: 0 10px 28px rgba(15, 23, 42, 0.08);"
            ):
                ui.label("Priority Distribution").classes("text-lg font-semibold text-slate-800")
                ui.echart({
                    "tooltip": {"trigger": "item"},
                    "series": [
                        {
                            "type": "pie",
                            "radius": "65%",
                            "data": [
                                {"value": priority_distribution["high"], "name": "High"},
                                {"value": priority_distribution["medium"], "name": "Medium"},
                                {"value": priority_distribution["low"], "name": "Low"},
                            ],
                        }
                    ],
                }).style("height: 350px; width: 100%;")

        if selected_semester == "All semesters" and semester_statistics:
            with ui.card().style(card_style()):
                ui.label("Semester Credits").classes("text-lg font-semibold text-slate-800")
                ui.echart({
                    "tooltip": {"trigger": "axis"},
                    "legend": {"data": ["Planned", "Completed"]},
                    "xAxis": {
                        "type": "category",
                        "data": [item["semester"] for item in semester_statistics],
                    },
                    "yAxis": {"type": "value"},
                    "series": [
                        {
                            "name": "Planned",
                            "type": "bar",
                            "data": [item["planned_credits"] for item in semester_statistics],
                        },
                        {
                            "name": "Completed",
                            "type": "bar",
                            "data": [item["completed_credits"] for item in semester_statistics],
                        },
                    ],
                }).style("height: 350px; width: 100%;")

            ui.label("Semester Detail View").classes("text-lg font-semibold text-slate-800")
            for item in semester_statistics:
                with ui.card().style(card_style()):
                    ui.label(str(item["semester"])).classes("font-semibold text-slate-800")
                    ui.label(f"Modules: {item['modules']}").classes("text-sm text-slate-600")
                    ui.label(f"Completed modules: {item['completed_modules']}").classes("text-sm text-slate-600")
                    ui.label(f"Planned credits: {item['planned_credits']}").classes("text-sm text-slate-600")
                    ui.label(f"Completed credits: {item['completed_credits']}").classes("text-sm text-slate-600")

        ui.label("Tasks per Subject (Detail View)").classes("text-lg font-semibold text-slate-800")

        if not subjects:
            ui.label("No subjects available.").classes("text-slate-500")
        else:
            for subject in subjects:
                subject_tasks = [task for task in tasks if task.subject_id == subject.id]
                with ui.card().style(card_style()):
                    ui.label(subject.name).classes("text-lg font-semibold text-slate-800")
                    with ui.row().classes("items-center").style("gap: 8px; flex-wrap: wrap;"):
                        ui.label(f"ECTS: {subject.ects}").style(
                            "background:#eff6ff; color:#1d4ed8; padding:4px 10px; border-radius:999px; "
                            "font-size:12px; font-weight:600;"
                        )
                        ui.label(subject.semester).style(
                            "background:#f5f3ff; color:#6d28d9; padding:4px 10px; border-radius:999px; "
                            "font-size:12px; font-weight:600;"
                        )
                        ui.label("Completed" if subject.is_completed else "Not completed").style(
                            status_style(subject.is_completed)
                        )

                    ui.label(f"Tasks: {len(subject_tasks)}").classes("text-sm text-slate-600")
                    ui.label(
                        f"Planned minutes: {sum(task.estimated_minutes for task in subject_tasks)}"
                    ).classes("text-sm text-slate-600")

        ui.label("Completed Modules").classes("text-lg font-semibold text-slate-800")

        if not completed_subjects:
            ui.label("No completed modules yet.").classes("text-slate-500")
        else:
            for subject in completed_subjects:
                with ui.card().style(card_style()):
                    ui.label(subject.name).classes("text-lg font-semibold text-slate-800")
                    ui.label(f"Semester: {subject.semester}").classes("text-sm text-slate-600")
                    ui.label(f"ECTS: {subject.ects}").classes("text-sm text-slate-600")
