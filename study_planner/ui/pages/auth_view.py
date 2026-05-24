from nicegui import ui


def build_login_view(on_login, on_register):
    with ui.column().style(
        "min-height: 100vh; width: 100%; align-items: center; justify-content: center; padding: 28px;"
    ):
        with ui.card().style(
            "width: min(460px, 92vw); border-radius: 24px; padding: 28px; "
            "background: white; box-shadow: 0 18px 40px rgba(15, 23, 42, 0.12);"
        ):
            ui.label("🔐 StudyPlanner Login").classes("text-3xl font-bold text-slate-800")
            ui.label("Log in or create a new account to access your study planner.").classes("text-slate-500")

            username_input = ui.input("Username").classes("w-full")
            password_input = ui.input(
                "Password",
                password=True,
                password_toggle_button=True,
            ).classes("w-full")
            confirm_password_input = ui.input(
                "Confirm password (only for registration)",
                password=True,
                password_toggle_button=True,
            ).classes("w-full")

            with ui.row().classes("w-full").style("gap: 12px; flex-wrap: wrap;"):
                ui.button("Log in", on_click=on_login).classes("w-full").props("color=primary")
                ui.button("Register", on_click=on_register).classes("w-full").props("outline color=primary")

            with ui.card().style(
                "width: 100%; margin-top: 8px; border-radius: 16px; padding: 14px; "
                "background: #f8fafc; box-shadow: none;"
            ):
                ui.label("Registration note").classes("text-sm font-semibold text-slate-700")
                ui.label("For a new account, enter username, password, and confirm password.").classes(
                    "text-sm text-slate-600"
                )
                ui.label("For login, only username and password are required.").classes("text-sm text-slate-600")

    return {
        "username_input": username_input,
        "password_input": password_input,
        "confirm_password_input": confirm_password_input,
    }


def build_app_header(app_title: str, username: str, on_logout) -> None:
    with ui.card().style(
        "width: 100%; border-radius: 24px; padding: 26px; "
        "background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%); "
        "color: white; box-shadow: 0 18px 40px rgba(79, 70, 229, 0.22);"
    ):
        with ui.row().style(
            "width: 100%; justify-content: space-between; align-items: flex-start; gap: 16px; flex-wrap: wrap;"
        ):
            with ui.column().classes("gap-2"):
                ui.label(f"📚 {app_title}").classes("text-4xl font-bold")
                ui.label(
                    "Organize subjects, tasks, credits, and semester progress in one clear workspace."
                ).classes("text-base opacity-90")

                with ui.row().classes("w-full").style("gap: 10px; margin-top: 12px; flex-wrap: wrap;"):
                    ui.label("✨ Cleaner workflow").style(
                        "background: rgba(255,255,255,0.18); padding: 6px 12px; border-radius: 999px;"
                    )
                    ui.label("📊 Better statistics").style(
                        "background: rgba(255,255,255,0.18); padding: 6px 12px; border-radius: 999px;"
                    )
                    ui.label("🗓️ Weekly planning").style(
                        "background: rgba(255,255,255,0.18); padding: 6px 12px; border-radius: 999px;"
                    )

            with ui.column().style("align-items: flex-end; gap: 8px;"):
                ui.label(f"Logged in as: {username}").classes("text-sm opacity-90")
                ui.button("Logout", on_click=on_logout).props("outline color=white")
