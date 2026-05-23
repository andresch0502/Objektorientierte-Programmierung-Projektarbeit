from nicegui import app


DEMO_USERNAME = "admin"
DEMO_PASSWORD = "studyplanner123"


def is_logged_in() -> bool:
    return bool(app.storage.user.get("authenticated", False))


def login(username: str, password: str) -> bool:
    if username == DEMO_USERNAME and password == DEMO_PASSWORD:
        app.storage.user["authenticated"] = True
        app.storage.user["username"] = username
        return True
    return False


def logout() -> None:
    app.storage.user["authenticated"] = False
    app.storage.user["username"] = ""


def get_logged_in_username() -> str:
    return str(app.storage.user.get("username", ""))
