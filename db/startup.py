from .models import Base
from .engine import engine


def create_db_tables() -> None:
    Base.metadata.create_all(engine)
