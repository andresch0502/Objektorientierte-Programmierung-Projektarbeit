from nicegui import ui


SEMESTER_OPTIONS = [
    "All semesters",
    "Semester 1",
    "Semester 2",
    "Semester 3",
    "Semester 4",
    "Semester 5",
    "Semester 6",
]


def section_title(title: str, subtitle: str = "") -> None:
    ui.label(title).classes("text-xl font-semibold text-slate-800")
    if subtitle:
        ui.label(subtitle).classes("text-sm text-slate-500")


def card_style() -> str:
    return (
        "width: 100%; border-radius: 20px; padding: 18px; "
        "box-shadow: 0 10px 28px rgba(15, 23, 42, 0.08); "
        "border: 1px solid rgba(148, 163, 184, 0.15);"
    )


def info_card(title: str, value: str, background: str, text_color: str = "#0f172a") -> None:
    with ui.card().style(
        f"flex: 1; min-width: 180px; border-radius: 18px; padding: 16px; "
        f"background: {background}; color: {text_color}; "
        "box-shadow: 0 10px 26px rgba(15, 23, 42, 0.08);"
    ):
        ui.label(title).classes("text-sm opacity-80")
        ui.label(value).classes("text-3xl font-bold")


def priority_style(priority: str) -> str:
    mapping = {
        "high": "background:#fee2e2;color:#b91c1c;",
        "medium": "background:#fef3c7;color:#b45309;",
        "low": "background:#dcfce7;color:#15803d;",
    }
    base = "padding: 4px 10px; border-radius: 999px; font-size: 12px; font-weight: 600;"
    return base + mapping.get(priority, "background:#e2e8f0;color:#334155;")


def status_style(is_completed: bool) -> str:
    if is_completed:
        return (
            "padding: 4px 10px; border-radius: 999px; font-size: 12px; "
            "font-weight: 600; background:#dcfce7; color:#15803d;"
        )
    return (
        "padding: 4px 10px; border-radius: 999px; font-size: 12px; "
        "font-weight: 600; background:#e2e8f0; color:#475569;"
    )
