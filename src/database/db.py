from sqlmodel import SQLModel, create_engine
from src.config import settings

engine = create_engine(url=settings.database_connection_string, echo=settings.database_echo)

def initialize_db():
    SQLModel.metadata.create_all(engine)
