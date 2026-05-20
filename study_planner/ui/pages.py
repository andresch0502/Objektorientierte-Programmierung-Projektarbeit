from datetime import date, timedelta

from nicegui import ui

from study_planner.ui.controllers import (
    add_subject,
    add_task,
    complete_task,
    edit_subject,
    export_subjects_csv,
    export_tasks_csv,
    get_app_title,
    get_credit_summary,
    get_priority_distribution,
    get_subjects,
    get_task_progress,
    get_tasks,
    get_tasks_per_subject,
    get_urgent_tasks,
    remove_subject,
)


def show_home_page() -> None:
    ui.query("body").style("background-color: #f5f7fb;")

    with ui.column().style("max-width: 1200px; margin: 0 auto; padding: 24px; width: 100%; gap: 20px;"):
        ui.label(get_app_title()).classes("text-3xl font-bold")
        ui.label("Plan your subjects, tasks, priorities, and weekly workload.").classes("text-gray-600")

        edit_subject_state = {"id": None}

        def section_title(title: str, subtitle: str = "") -> None:
            ui.label(title).classes("text-xl font-semibold")
            if subtitle:
                ui.label(subtitle).classes("text-sm text-gray-500")

        with ui.tabs().classes("w-full") as tabs:
            dashboard_tab = ui.tab("Dashboard")
            subjects_tab = ui.tab("Subjects")
            tasks_tab = ui.tab("Tasks")
            statistics_tab = ui.tab("Statistics")

        with ui.tab_panels(tabs, value=dashboard_tab).classes("w-full"):
            with ui.tab_panel(dashboard_tab):
                dashboard_semester_select = ui.select(
                    options=[
                        "All semesters",
                        "Semester 1",
                        "Semester 2",
                        "Semester 3",
                        "Semester 4",
                        "Semester 5",
                        "Semester 6",
                    ],
                    label="Semester filter",
                    value="All semesters",
                    on_change=lambda _: refresh_dashboard(),
                ).classes("w-full max-w-xs")
                credit_box = ui.column().classes("w-full")
                progress_box = ui.column().classes("w-full")
                urgent_task_list = ui.column().classes("w-full")
                week_overview_box = ui.column().classes("w-full")

            with ui.tab_panel(subjects_tab):
                with ui.card().classes("w-full"):
                    section_title("Add New Subject")
                    subject_name_input = ui.input("Subject name").classes("w-full")
                    subject_ects_input = ui.input("ECTS").classes("w-full")
                    subject_semester_select = ui.select(
                        options=[
                            "Semester 1",
                            "Semester 2",
                            "Semester 3",
                            "Semester 4",
                            "Semester 5",
                            "Semester 6",
                        ],
                        label="Semester",
                        value="Semester 1",
                    ).classes("w-full")
                    subject_moodle_link_input = ui.input("Moodle link (optional)").classes("w-full")
                    add_subject_button = ui.button("Add subject").classes("w-full")

                with ui.card().classes("w-full"):
                    section_title("Existing Subjects")
                    subject_list = ui.column().classes("w-full")

            with ui.tab_panel(tasks_tab):
                with ui.card().classes("w-full"):
                    section_title(
                        "Add Task",
                        "Mandatory: Subject, Task title, Priority. Optional: deadline, planned date, estimated minutes, notes.",
                    )

                    task_subject_select = ui.select(options={}, label="Subject *").classes("w-full")
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

                    ui.label("Deadline (optional)").classes("text-sm text-gray-600")
                    with ui.row().classes("w-full"):
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

                    ui.label("Planned date (optional)").classes("text-sm text-gray-600")
                    with ui.row().classes("w-full"):
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
                    add_task_button = ui.button("Add task").classes("w-full")

                with ui.card().classes("w-full"):
                    section_title("Task Overview")
                    task_list = ui.column().classes("w-full")

            with ui.tab_panel(statistics_tab):
                with ui.card().classes("w-full"):
                    section_title("Export", "Export subjects and tasks as CSV files for Excel.")
                    export_subjects_button = ui.button("Export Subjects CSV").classes("w-full")
                    export_tasks_button = ui.button("Export Tasks CSV").classes("w-full")

                statistics_box = ui.column().classes("w-full")

        with ui.dialog() as edit_subject_dialog, ui.card().classes("w-full"):
            ui.label("Edit Subject").classes("text-xl font-semibold")
            edit_subject_name_input = ui.input("Subject name").classes("w-full")
            edit_subject_ects_input = ui.input("ECTS").classes("w-full")
            edit_subject_semester_select = ui.select(
                options=[
                    "Semester 1",
                    "Semester 2",
                    "Semester 3",
                    "Semester 4",
                    "Semester 5",
                    "Semester 6",
                ],
                label="Semester",
                value="Semester 1",
            ).classes("w-full")
            edit_subject_moodle_link_input = ui.input("Moodle link (optional)").classes("w-full")
            edit_subject_completed_checkbox = ui.checkbox("Module completed")
            with ui.row().classes("w-full justify-end"):
                cancel_edit_subject_button = ui.button("Cancel")
                save_edit_subject_button = ui.button("Save changes")

        def get_subject_name_map() -> dict[int, str]:
            return {
                subject.id: subject.name
                for subject in get_subjects()
                if subject.id is not None
            }

        def build_optional_date(day_value: str | None, month_value: str | None, year_value: str | None, label: str) -> date | None:
            if not day_value and not month_value and not year_value:
                return None

            if not day_value or not month_value or not year_value:
                ui.notify(f"Please complete day, month, and year for the {label}.")
                raise ValueError(label)

            try:
                return date(int(year_value), int(month_value), int(day_value))
            except ValueError:
                ui.notify(f"Please select a valid {label}.")
                raise

        def refresh_subject_options() -> None:
            options = get_subject_name_map()
            task_subject_select.options = options
            task_subject_select.update()

        def open_edit_subject_dialog(subject_id: int) -> None:
            subjects = get_subjects()
            subject = next((item for item in subjects if item.id == subject_id), None)
            if subject is None:
                ui.notify("Subject not found.")
                return

            edit_subject_state["id"] = subject.id
            edit_subject_name_input.value = subject.name
            edit_subject_ects_input.value = str(subject.ects)
            edit_subject_semester_select.value = subject.semester
            edit_subject_moodle_link_input.value = subject.moodle_link
            edit_subject_completed_checkbox.value = subject.is_completed
            edit_subject_dialog.open()

        def refresh_subject_list() -> None:
            subject_list.clear()
            with subject_list:
                subjects = get_subjects()
                if not subjects:
                    ui.label("No subjects added yet.").classes("text-gray-500")
                    return

                for subject in subjects:
                    with ui.card().classes("w-full"):
                        with ui.row().style("width: 100%; justify-content: space-between; align-items: center; gap: 12px;"):
                            with ui.column().classes("gap-1"):
                                ui.label(subject.name).classes("font-medium")
                                ui.label(f"ECTS: {subject.ects}").classes("text-sm text-gray-600")
                                ui.label(f"Semester: {subject.semester}").classes("text-sm text-gray-600")
                                ui.label(
                                    "Completed" if subject.is_completed else "Not completed"
                                ).classes("text-sm text-gray-600")
                                if subject.moodle_link:
                                    ui.link("Open Moodle", subject.moodle_link, new_tab=True).classes("text-sm")

                            with ui.row().classes("gap-2"):
                                if subject.id is not None:
                                    ui.button(
                                        "Edit",
                                        on_click=lambda subject_id=subject.id: open_edit_subject_dialog(subject_id),
                                    )
                                    ui.button(
                                        "Delete",
                                        on_click=lambda subject_id=subject.id: handle_remove_subject(subject_id),
                                    ).props("color=negative")

        def refresh_credit_box() -> None:
            credit_box.clear()
            with credit_box:
                selected_semester = dashboard_semester_select.value or "All semesters"
                section_title("Credits Overview", f"Showing credits for: {selected_semester}")
                credits = get_credit_summary(selected_semester)

                with ui.row().classes("w-full"):
                    with ui.card().style("flex: 1;"):
                        ui.label("Planned Credits").classes("text-sm text-gray-500")
                        ui.label(str(credits["planned"])).classes("text-2xl font-bold")

                    with ui.card().style("flex: 1;"):
                        ui.label("Completed Credits").classes("text-sm text-gray-500")
                        ui.label(str(credits["completed"])).classes("text-2xl font-bold")

                    with ui.card().style("flex: 1;"):
                        ui.label("Open Credits").classes("text-sm text-gray-500")
                        ui.label(str(credits["open"])).classes("text-2xl font-bold")

        def refresh_progress_box() -> None:
            progress_box.clear()
            with progress_box:
                section_title("Progress")
                progress = get_task_progress()
                subjects = get_subjects()

                with ui.row().classes("w-full"):
                    with ui.card().style("flex: 1;"):
                        ui.label("Subjects").classes("text-sm text-gray-500")
                        ui.label(str(len(subjects))).classes("text-2xl font-bold")

                    with ui.card().style("flex: 1;"):
                        ui.label("Total tasks").classes("text-sm text-gray-500")
                        ui.label(str(progress["total"])).classes("text-2xl font-bold")

                    with ui.card().style("flex: 1;"):
                        ui.label("Completed").classes("text-sm text-gray-500")
                        ui.label(str(progress["completed"])).classes("text-2xl font-bold")

                    with ui.card().style("flex: 1;"):
                        ui.label("Open").classes("text-sm text-gray-500")
                        ui.label(str(progress["open"])).classes("text-2xl font-bold")

        def refresh_urgent_task_list() -> None:
            urgent_task_list.clear()
            with urgent_task_list:
                section_title("Urgent Tasks")
                urgent_tasks = get_urgent_tasks()
                subject_names = get_subject_name_map()

                if not urgent_tasks:
                    ui.label("No urgent tasks at the moment.").classes("text-gray-500")
                    return

                for task in urgent_tasks:
                    with ui.card().classes("w-full"):
                        ui.label(task.title).classes("font-medium")
                        if task.subject_id in subject_names:
                            ui.label(f"Subject: {subject_names[task.subject_id]}").classes("text-sm text-gray-600")
                        if task.deadline:
                            ui.label(f"Deadline: {task.deadline}").classes("text-sm text-red-600")
                        ui.label(f"Priority: {task.priority.capitalize()}").classes("text-sm text-gray-600")
                        if task.estimated_minutes:
                            ui.label(f"Planned effort: {task.estimated_minutes} minutes").classes("text-sm text-gray-600")
                        if task.notes:
                            ui.label(task.notes).classes("text-sm text-gray-500")

        def refresh_week_overview() -> None:
            week_overview_box.clear()
            with week_overview_box:
                section_title("Weekly Overview", "Tasks planned for the next 7 days")
                tasks = get_tasks()
                subject_names = get_subject_name_map()
                start_day = date.today()

                for offset in range(7):
                    current_day = start_day + timedelta(days=offset)
                    day_tasks = [
                        task for task in tasks
                        if task.planned_date == current_day
                    ]

                    with ui.card().classes("w-full"):
                        ui.label(current_day.strftime("%A, %Y-%m-%d")).classes("font-medium")

                        if not day_tasks:
                            ui.label("No tasks planned.").classes("text-sm text-gray-500")
                            continue

                        for task in day_tasks:
                            subject_text = subject_names.get(task.subject_id, "No subject")
                            ui.label(
                                f"- {task.title} | {subject_text} | "
                                f"{task.priority.capitalize()} | {task.estimated_minutes} min"
                            ).classes("text-sm text-gray-700")

        def refresh_task_list() -> None:
            task_list.clear()
            with task_list:
                tasks = get_tasks()
                subject_names = get_subject_name_map()

                if not tasks:
                    ui.label("No tasks added yet.").classes("text-gray-500")
                    return

                for task in tasks:
                    with ui.card().classes("w-full"):
                        with ui.row().style("width: 100%; justify-content: space-between; align-items: start; gap: 12px;"):
                            with ui.column().classes("gap-1"):
                                title_prefix = "✅ " if task.is_completed else ""
                                ui.label(f"{title_prefix}{task.title}").classes("font-medium")

                                if task.subject_id in subject_names:
                                    ui.label(f"Subject: {subject_names[task.subject_id]}").classes("text-sm text-gray-600")

                                ui.label(f"Priority: {task.priority.capitalize()}").classes("text-sm text-gray-600")

                                if task.deadline:
                                    ui.label(f"Deadline: {task.deadline}").classes("text-sm text-gray-600")

                                if task.planned_date:
                                    ui.label(f"Planned date: {task.planned_date}").classes("text-sm text-gray-600")

                                if task.estimated_minutes:
                                    ui.label(f"Estimated time: {task.estimated_minutes} minutes").classes("text-sm text-gray-600")

                                if task.notes:
                                    ui.label(task.notes).classes("text-sm text-gray-500")

                            if not task.is_completed and task.id is not None:
                                ui.button(
                                    "Complete",
                                    on_click=lambda task_id=task.id: handle_complete_task(task_id),
                                )

        def refresh_statistics_box() -> None:
            statistics_box.clear()
            with statistics_box:
                section_title("Statistics")

                tasks = get_tasks()
                subjects = get_subjects()
                tasks_per_subject = get_tasks_per_subject()
                priority_distribution = get_priority_distribution()

                if not tasks and not subjects:
                    ui.label("No statistics available yet.").classes("text-gray-500")
                    return

                with ui.row().classes("w-full"):
                    with ui.card().style("flex: 1;"):
                        ui.label("Total Subjects").classes("text-sm text-gray-500")
                        ui.label(str(len(subjects))).classes("text-2xl font-bold")

                    with ui.card().style("flex: 1;"):
                        ui.label("Total Tasks").classes("text-sm text-gray-500")
                        ui.label(str(len(tasks))).classes("text-2xl font-bold")

                    with ui.card().style("flex: 1;"):
                        ui.label("Total Planned Minutes").classes("text-sm text-gray-500")
                        ui.label(str(sum(task.estimated_minutes for task in tasks))).classes("text-2xl font-bold")

                ui.separator()

                with ui.row().classes("w-full").style("gap: 20px; flex-wrap: wrap;"):
                    with ui.card().style("flex: 1; min-width: 320px;"):
                        ui.label("Tasks per Subject").classes("text-lg font-semibold")
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

                    with ui.card().style("flex: 1; min-width: 320px;"):
                        ui.label("Priority Distribution").classes("text-lg font-semibold")
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

                ui.separator()
                ui.label("Tasks per Subject (Detail View)").classes("text-lg font-semibold")

                if not subjects:
                    ui.label("No subjects available.").classes("text-gray-500")
                else:
                    for subject in subjects:
                        subject_tasks = [
                            task for task in tasks
                            if task.subject_id == subject.id
                        ]
                        with ui.card().classes("w-full"):
                            ui.label(subject.name).classes("font-medium")
                            ui.label(f"ECTS: {subject.ects}").classes("text-sm text-gray-600")
                            ui.label(f"Semester: {subject.semester}").classes("text-sm text-gray-600")
                            ui.label(
                                "Completed" if subject.is_completed else "Not completed"
                            ).classes("text-sm text-gray-600")
                            ui.label(f"Tasks: {len(subject_tasks)}").classes("text-sm text-gray-600")
                            ui.label(
                                f"Planned minutes: {sum(task.estimated_minutes for task in subject_tasks)}"
                            ).classes("text-sm text-gray-600")

        def refresh_dashboard() -> None:
            refresh_credit_box()
            refresh_progress_box()
            refresh_urgent_task_list()
            refresh_week_overview()

        def handle_add_subject() -> None:
            if not subject_name_input.value:
                ui.notify("Please enter a subject name.")
                return

            try:
                ects = int(subject_ects_input.value or 0)
                if ects < 0:
                    ui.notify("ECTS must be 0 or greater.")
                    return
            except ValueError:
                ui.notify("Please enter a valid ECTS number.")
                return

            add_subject(
                subject_name_input.value,
                ects,
                subject_semester_select.value or "Semester 1",
                subject_moodle_link_input.value or "",
            )
            subject_name_input.value = ""
            subject_ects_input.value = ""
            subject_semester_select.value = "Semester 1"
            subject_moodle_link_input.value = ""
            refresh_subject_list()
            refresh_subject_options()
            refresh_dashboard()
            refresh_statistics_box()
            ui.notify("Subject added.")

        def handle_save_edited_subject() -> None:
            if edit_subject_state["id"] is None:
                ui.notify("No subject selected.")
                return

            if not edit_subject_name_input.value:
                ui.notify("Please enter a subject name.")
                return

            try:
                ects = int(edit_subject_ects_input.value or 0)
                if ects < 0:
                    ui.notify("ECTS must be 0 or greater.")
                    return
            except ValueError:
                ui.notify("Please enter a valid ECTS number.")
                return

            edit_subject(
                edit_subject_state["id"],
                edit_subject_name_input.value,
                ects,
                edit_subject_semester_select.value or "Semester 1",
                edit_subject_moodle_link_input.value or "",
                bool(edit_subject_completed_checkbox.value),
            )
            edit_subject_dialog.close()
            refresh_subject_list()
            refresh_subject_options()
            refresh_dashboard()
            refresh_statistics_box()
            ui.notify("Subject updated.")

        def handle_remove_subject(subject_id: int) -> None:
            tasks = get_tasks()
            linked_tasks = [task for task in tasks if task.subject_id == subject_id]

            if linked_tasks:
                ui.notify("You cannot delete a subject that still has tasks.")
                return

            remove_subject(subject_id)
            refresh_subject_list()
            refresh_subject_options()
            refresh_dashboard()
            refresh_statistics_box()
            ui.notify("Subject deleted.")

        def handle_add_task() -> None:
            if not task_subject_select.value:
                ui.notify("Please select a subject.")
                return

            if not task_title_input.value:
                ui.notify("Please enter a task title.")
                return

            try:
                deadline = build_optional_date(
                    deadline_day_select.value,
                    deadline_month_select.value,
                    deadline_year_select.value,
                    "deadline",
                )
            except ValueError:
                return

            try:
                planned_date = build_optional_date(
                    planned_day_select.value,
                    planned_month_select.value,
                    planned_year_select.value,
                    "planned date",
                )
            except ValueError:
                return

            try:
                estimated_minutes = int(estimated_minutes_input.value or 0)
                if estimated_minutes < 0:
                    ui.notify("Estimated minutes must be 0 or greater.")
                    return
            except ValueError:
                ui.notify("Please enter a valid number of minutes.")
                return

            add_task(
                task_title_input.value,
                deadline,
                planned_date,
                estimated_minutes,
                priority_select.value or "medium",
                task_notes_input.value or "",
                task_subject_select.value,
            )
            task_title_input.value = ""
            deadline_day_select.value = None
            deadline_month_select.value = None
            deadline_year_select.value = None
            planned_day_select.value = None
            planned_month_select.value = None
            planned_year_select.value = None
            estimated_minutes_input.value = ""
            priority_select.value = "medium"
            task_notes_input.value = ""
            task_subject_select.value = None
            refresh_task_list()
            refresh_dashboard()
            refresh_statistics_box()
            ui.notify("Task added.")

        def handle_complete_task(task_id: int) -> None:
            complete_task(task_id)
            refresh_task_list()
            refresh_dashboard()
            refresh_statistics_box()
            ui.notify("Task completed.")

        def handle_export_subjects() -> None:
            path = export_subjects_csv()
            ui.notify(f"Subjects exported to: {path}")

        def handle_export_tasks() -> None:
            path = export_tasks_csv()
            ui.notify(f"Tasks exported to: {path}")

        add_subject_button.on("click", lambda: handle_add_subject())
        add_task_button.on("click", lambda: handle_add_task())
        export_subjects_button.on("click", lambda: handle_export_subjects())
        export_tasks_button.on("click", lambda: handle_export_tasks())
        cancel_edit_subject_button.on("click", lambda: edit_subject_dialog.close())
        save_edit_subject_button.on("click", lambda: handle_save_edited_subject())

        refresh_subject_options()
        refresh_subject_list()
        refresh_task_list()
        refresh_dashboard()
        refresh_statistics_box()
