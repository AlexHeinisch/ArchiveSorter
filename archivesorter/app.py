from sqlmodel import Session
from typer import Typer
from archivesorter.file_manager import (
    extract_file_info_by_path,
    get_all_file_paths_by_root_folder,
)
from config import settings
from database.db import initialize_db, engine
from rich.progress import track


app = Typer(name=settings.app_name)
initialize_db()


@app.command()
def load(input_folder_path: str):
    print('Start loading files...')
    with Session(engine) as session:
        for file in track(list(get_all_file_paths_by_root_folder(input_folder_path))):
            file_info = extract_file_info_by_path(file)
            session.add(file_info)
            session.commit()


@app.command()
def categorize():
    print('Start categorizing...')


@app.command()
def info():
    print('Printing info...')


@app.command()
def organize(output_folder_path: str):
    print('Start organizing...')


if __name__ == '__main__':
    app()
