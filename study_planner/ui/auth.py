from nicegui import app

from study_planner.data_access.db import Database
from study_planner.services.user_service import UserService


database = Database()
user_service = UserService()


def is_logged_in() -> bool:
    return bool(app.storage.user.get("authenticated", False))


def login(username: str, password: str) -> bool:
    with database.session_scope() as session:
        user = user_service.authenticate_user(session, username, password)

    if user is None:
        return False

    app.storage.user["authenticated"] = True
    app.storage.user["username"] = user.username
    return True


def register(username: str, password: str) -> tuple[bool, str]:
    with database.session_scope() as session:
        return user_service.register_user(session, username, password)


def logout() -> None:
    app.storage.user["authenticated"] = False
    app.storage.user["username"] = ""


def get_logged_in_username() -> str:
    return str(app.storage.user.get("username", ""))
