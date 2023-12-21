from typing import Annotated
from sqlmodel import Session, func, select
import typer
from archivesorter.categorizer import evaluate_category
from archivesorter.database.models import FileInfo
from archivesorter.file_manager import (
    extract_file_info_by_path,
    extract_image_creation_date_from_metadata_if_image,
    get_all_file_paths_by_root_folder,
)
from config import settings
from database.db import clear_db, initialize_db, engine
from rich.progress import track
from rich import print
from archivesorter.manager_app import app as manager_app


app = typer.Typer(name=settings.app_name)
app.add_typer(manager_app, name='manage')
initialize_db()


@app.command()
def load(
    input_folder_path: Annotated[str, typer.Argument()],
    clear: Annotated[bool, typer.Option()] = False,
):
    if clear:
        print('[gray]Clearing database...[/gray]')
        clear_db()

    print('[gray]Start loading files...[/gray]')
    with Session(engine) as session:
        for file in track(list(get_all_file_paths_by_root_folder(input_folder_path))):
            file_info = extract_file_info_by_path(file)
            file_info.photo_created = (
                extract_image_creation_date_from_metadata_if_image(file)
            )
            file_info.evaluated_datetime = (
                file_info.photo_created or file_info.file_created
            )
            session.add(file_info)
            session.commit()


@app.command()
def clear_database():
    print('[gray]Clearing database...[/gray]')
    clear_db()


@app.command()
def categorize():
    with Session(engine) as session:
        for fi in track(
            session.exec(select(FileInfo)),
            total=session.exec(select(func.count(FileInfo.id))).one(),
        ):
            category = evaluate_category(fi)
            fi.evaluated_category = category
            session.add(fi)
        session.commit()


@app.command()
def organize(output_folder_path: str):
    print('Start organizing...')


if __name__ == '__main__':
    app()
