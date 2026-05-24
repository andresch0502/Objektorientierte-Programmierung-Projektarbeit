import hashlib
import hmac
import secrets

from sqlmodel import Session, select

from study_planner.domain.models import User


class UserService:
    def get_user_by_username(self, session: Session, username: str) -> User | None:
        statement = select(User).where(User.username == username)
        return session.exec(statement).first()

    def register_user(self, session: Session, username: str, password: str) -> tuple[bool, str]:
        normalized_username = username.strip()

        if len(normalized_username) < 3:
            return False, "Username must be at least 3 characters long."

        if len(password) < 6:
            return False, "Password must be at least 6 characters long."

        existing_user = self.get_user_by_username(session, normalized_username)
        if existing_user is not None:
            return False, "Username already exists."

        password_hash = self._hash_password(password)

        user = User(
            username=normalized_username,
            password_hash=password_hash,
        )
        session.add(user)
        session.commit()
        session.refresh(user)

        return True, "Registration successful."

    def authenticate_user(self, session: Session, username: str, password: str) -> User | None:
        normalized_username = username.strip()
        user = self.get_user_by_username(session, normalized_username)

        if user is None:
            return None

        if not self._verify_password(password, user.password_hash):
            return None

        return user

    def _hash_password(self, password: str) -> str:
        salt = secrets.token_hex(16)
        hashed = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt.encode("utf-8"),
            100_000,
        ).hex()
        return f"{salt}${hashed}"

    def _verify_password(self, password: str, stored_password_hash: str) -> bool:
        try:
            salt, expected_hash = stored_password_hash.split("$", maxsplit=1)
        except ValueError:
            return False

        actual_hash = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt.encode("utf-8"),
            100_000,
        ).hex()

        return hmac.compare_digest(actual_hash, expected_hash)
