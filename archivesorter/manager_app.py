from rich import print
from typing import Annotated, List, Optional
from sqlmodel import Session, func, select
import typer
from archivesorter.database.db import engine
from archivesorter.database.models import FileInfo

app = typer.Typer()


def _print_file_info(fi: FileInfo):
    img_data = '(IM)' if fi.photo_created else ''
    cat_data = 'N/A' if not fi.evaluated_category else fi.evaluated_category
    print(
        f'ID: {fi.id:<6} :: [magenta]...{fi.source_path[-80:]:<83}[/magenta] category={cat_data:<20}  [yellow]{img_data:<4}[/yellow]'
    )


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


@app.command()
def show(
    limit: Annotated[Optional[int], typer.Option()] = None,
    offset: Annotated[Optional[int], typer.Option()] = None,
):
    with Session(engine) as session:
        query = select(FileInfo)
        if limit:
            query = query.limit(limit)
        if offset:
            query = query.offset(offset)
        for fi in session.exec(query).all():
            _print_file_info(fi)


@app.command()
def show_duplicates(
    limit: Annotated[Optional[int], typer.Option()] = None,
    offset: Annotated[Optional[int], typer.Option()] = None,
):
    with Session(engine) as session:
        query = (
            select(FileInfo.file_hash, func.count(FileInfo.id).label('hash_count'))
            .group_by(FileInfo.file_hash)
            .having(func.count(FileInfo.id) > 1)
            .order_by(FileInfo.file_hash)
        )
        if limit:
            query = query.limit(limit)
        if offset:
            query = query.offset(offset)
        idx = offset if offset else 1
        for hash, occurences in session.exec(query).all():
            print(f'[[{idx}]] {occurences} files with hash "{hash}":')
            for fi in session.exec(select(FileInfo).where(FileInfo.file_hash == hash)):
                _print_file_info(fi)
            print('')
            idx += 1


@app.command()
def delete(ids: Annotated[List[int], typer.Argument()]):
    with Session(engine) as session:
        for id in ids:
            entity = session.get(FileInfo, id)
            if entity:
                session.delete(entity)
                print(f'[green]File with id {id} deleted![/green]')
            else:
                print(f'[red]No file with id {id} found![/red]')
        session.commit()
