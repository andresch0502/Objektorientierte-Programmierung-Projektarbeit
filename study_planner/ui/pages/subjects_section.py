from nicegui import ui

from study_planner.ui.pages.shared import SEMESTER_OPTIONS, card_style, section_title, status_style


def build_subjects_tab(subjects_tab, on_add_subject):
    with ui.tab_panel(subjects_tab):
        with ui.card().style(card_style()):
            section_title("📚 Add New Subject", "Create a subject with credits, semester, and Moodle link.")
            subject_name_input = ui.input("Subject name").classes("w-full")
            subject_ects_input = ui.input("ECTS").classes("w-full")
            subject_semester_select = ui.select(
                options=SEMESTER_OPTIONS[1:],
                label="Semester",
                value="Semester 1",
            ).classes("w-full")
            subject_moodle_link_input = ui.input("Moodle link (optional)").classes("w-full")
            add_subject_button = ui.button("Add subject", on_click=on_add_subject).classes("w-full").props("color=primary")

        with ui.card().style(card_style()):
            section_title("🗂️ Existing Subjects", "Overview of all modules and their status.")
            subject_list = ui.column().classes("w-full")

    return {
        "subject_name_input": subject_name_input,
        "subject_ects_input": subject_ects_input,
        "subject_semester_select": subject_semester_select,
        "subject_moodle_link_input": subject_moodle_link_input,
        "add_subject_button": add_subject_button,
        "subject_list": subject_list,
    }


def build_edit_subject_dialog(on_save_subject):
    with ui.dialog() as edit_subject_dialog, ui.card().style(
        "width: min(560px, 90vw); border-radius: 22px; padding: 18px;"
    ):
        ui.label("✏️ Edit Subject").classes("text-xl font-semibold")
        edit_subject_name_input = ui.input("Subject name").classes("w-full")
        edit_subject_ects_input = ui.input("ECTS").classes("w-full")
        edit_subject_semester_select = ui.select(
            options=SEMESTER_OPTIONS[1:],
            label="Semester",
            value="Semester 1",
        ).classes("w-full")
        edit_subject_moodle_link_input = ui.input("Moodle link (optional)").classes("w-full")
        edit_subject_completed_checkbox = ui.checkbox("Module completed")
        with ui.row().classes("w-full justify-end").style("gap: 10px;"):
            cancel_edit_subject_button = ui.button("Cancel", on_click=lambda: edit_subject_dialog.close())
            save_edit_subject_button = ui.button("Save changes", on_click=on_save_subject).props("color=primary")

    return {
        "edit_subject_dialog": edit_subject_dialog,
        "edit_subject_name_input": edit_subject_name_input,
        "edit_subject_ects_input": edit_subject_ects_input,
        "edit_subject_semester_select": edit_subject_semester_select,
        "edit_subject_moodle_link_input": edit_subject_moodle_link_input,
        "edit_subject_completed_checkbox": edit_subject_completed_checkbox,
        "cancel_edit_subject_button": cancel_edit_subject_button,
        "save_edit_subject_button": save_edit_subject_button,
    }


def refresh_subject_list(subject_list, subjects, open_edit_subject_dialog, handle_remove_subject) -> None:
    subject_list.clear()
    with subject_list:
        if not subjects:
            ui.label("No subjects added yet.").classes("text-slate-500")
            return

        for subject in subjects:
            with ui.card().style(card_style()):
                with ui.row().style(
                    "width: 100%; justify-content: space-between; align-items: flex-start; gap: 12px;"
                ):
                    with ui.column().classes("gap-2"):
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

                        if subject.moodle_link:
                            ui.link("Open Moodle", subject.moodle_link, new_tab=True).classes("text-sm")

                    with ui.row().classes("gap-2"):
                        if subject.id is not None:
                            ui.button(
                                "Edit",
                                on_click=lambda subject_id=subject.id: open_edit_subject_dialog(subject_id),
                            ).props("outline color=primary")
                            ui.button(
                                "Delete",
                                on_click=lambda subject_id=subject.id: handle_remove_subject(subject_id),
                            ).props("color=negative")
