from study_planner.services.user_service import UserService


def test_register_user_success_creates_user_with_hashed_password(session):
    service = UserService()

    success, message = service.register_user(session, "  andres  ", "secret123")
    user = service.get_user_by_username(session, "andres")

    assert success is True
    assert message == "Registration successful."
    assert user is not None
    assert user.username == "andres"
    assert user.password_hash != "secret123"
    assert "$" in user.password_hash


def test_register_user_rejects_short_username(session):
    service = UserService()

    success, message = service.register_user(session, "ab", "secret123")

    assert success is False
    assert message == "Username must be at least 3 characters long."


def test_register_user_rejects_short_password(session):
    service = UserService()

    success, message = service.register_user(session, "andres", "123")

    assert success is False
    assert message == "Password must be at least 6 characters long."


def test_register_user_rejects_duplicate_username(session):
    service = UserService()
    service.register_user(session, "andres", "secret123")

    success, message = service.register_user(session, "andres", "another123")

    assert success is False
    assert message == "Username already exists."


def test_authenticate_user_returns_user_for_correct_password(session):
    service = UserService()
    service.register_user(session, "andres", "secret123")

    user = service.authenticate_user(session, "andres", "secret123")

    assert user is not None
    assert user.username == "andres"


def test_authenticate_user_returns_none_for_wrong_password(session):
    service = UserService()
    service.register_user(session, "andres", "secret123")

    user = service.authenticate_user(session, "andres", "wrong-password")

    assert user is None
