from typing import Optional
from sqlmodel import Field, SQLModel
from datetime import datetime


class FileInfo(SQLModel, table=True):
    # database id
    id: Optional[int] = Field(default=None, primary_key=True)

    # needs to be imported in first import step
    source_path: str
    file_last_modified: datetime
    file_created: datetime
    photo_created: Optional[datetime]
    file_hash: str

    # is computed in the categorization process
    evaluated_datetime: Optional[datetime] = Field(index=True)
    evaluated_category: Optional[str]
    computed_target_path: Optional[str] = Field(index=True)
