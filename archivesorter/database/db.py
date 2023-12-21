from sqlmodel import SQLModel, create_engine
from archivesorter.config import settings

engine = create_engine(
    url=settings.database_connection_string, echo=settings.database_echo
)


def clear_db():
    SQLModel.metadata.drop_all(engine)
    initialize_db()


def initialize_db():
    from archivesorter.database.models import FileInfo as FileInfo

    SQLModel.metadata.create_all(engine)
