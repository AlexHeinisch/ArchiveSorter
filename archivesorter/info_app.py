from sqlmodel import Session, func, select
import typer
from archivesorter.database.db import engine
from archivesorter.database.models import FileInfo

app = typer.Typer()


@app.command()
def count():
    with Session(engine) as session:
        cnt = session.exec(select(func.count(FileInfo.id))).one()
    print('Number of loaded files: ', cnt)


@app.command()
def count_exif():
    with Session(engine) as session:
        cnt = session.exec(
            select(func.count(FileInfo.photo_created)).where(
                FileInfo.photo_created is not None
            )
        ).one()
    print('Number of files with EXIF information: ', cnt)


@app.command()
def count_duplicates():
    with Session(engine) as session:
        base_query = select(func.count(FileInfo.id).label('hash_count')).group_by(
            FileInfo.file_hash
        )
        query = select(func.count(base_query.as_scalar())).where(
            base_query.c.hash_count > 1
        )
        cnt = session.exec(query).one()
    print('Number of duplicate files: ', cnt)
