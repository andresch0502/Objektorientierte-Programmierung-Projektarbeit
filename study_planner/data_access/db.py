from sqlmodel import SQLModel, create_engine


DATABASE_URL = "sqlite:///data/study_planner.db"

engine = create_engine(DATABASE_URL, echo=True)


def init_db() -> None:
    SQLModel.metadata.create_all(engine)
