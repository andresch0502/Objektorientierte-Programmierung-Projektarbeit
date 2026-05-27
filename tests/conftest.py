import pytest
from sqlmodel import SQLModel, Session, create_engine


@pytest.fixture()
def session():
    """Creates a clean in-memory test database for each test."""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
