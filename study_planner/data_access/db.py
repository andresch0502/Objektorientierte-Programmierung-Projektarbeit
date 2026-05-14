from __future__ import annotations

from contextlib import contextmanager
from pathlib import Path
from typing import Iterator, Optional

from sqlmodel import SQLModel, Session, create_engine


class Database:
    def __init__(self, database_url: Optional[str] = None, *, echo: bool = False) -> None:
        self._database_url = database_url or self._default_sqlite_url()
        self._engine = create_engine(
            self._database_url,
            echo=echo,
            connect_args={"check_same_thread": False},
        )

    @staticmethod
    def _default_sqlite_url() -> str:
        Path("data").mkdir(parents=True, exist_ok=True)
        return "sqlite:///data/study_planner.db"

    @property
    def engine(self):
        return self._engine

    def init_schema(self) -> None:
        SQLModel.metadata.create_all(self._engine)

    @contextmanager
    def session_scope(self) -> Iterator[Session]:
        session = Session(self._engine, expire_on_commit=False)
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
