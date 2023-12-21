from sqlmodel import SQLModel, create_engine
from archivesorter.config import settings

engine = create_engine(url=settings.database_connection_string, echo=settings.database_echo)

def initialize_db():
    import archivesorter.database.models
    SQLModel.metadata.create_all(engine)
