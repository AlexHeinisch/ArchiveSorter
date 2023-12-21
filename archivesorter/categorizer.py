from datetime import datetime
from archivesorter.database.models import FileInfo


def evaluate_date(info: FileInfo) -> datetime:
    ...


def evaluate_category(info: FileInfo) -> str:
    ...


def compute_target_path(info: FileInfo) -> str:
    ...
