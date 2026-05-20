from study_planner.data_access.db import Database
from study_planner.data_access.seed import seed_demo_data
import study_planner.domain.models  # ensures SQLModel tables are registered
from study_planner.ui.pages import show_home_page


database = Database()


def setup_app() -> None:
    database.init_schema()

    with database.session_scope() as session:
        seed_demo_data(session)

    show_home_page()
