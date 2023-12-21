from typer import Typer
from config import settings
from database.db import initialize_db


app = Typer(name=settings.app_name)
initialize_db()

@app.command()
def load(input_folder_path: str):
    print('Start loading files...')

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
