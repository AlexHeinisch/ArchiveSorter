from sqlmodel import Session, func, select
import typer
from archivesorter.database.db import engine
from archivesorter.database.models import FileInfo

app = typer.Typer()


@app.command()
def num_files():
    with Session(engine) as session:
        cnt = session.exec(select(func.count(FileInfo.id))).one()
    print('Number of loaded files: ', cnt)
