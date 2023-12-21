from datetime import datetime
from typing import Generator
import os
from archivesorter.database.models import FileInfo


def get_all_file_paths_by_root_folder(
    root_folder_path: str,
) -> Generator[str, None, None]:
    extensions = '*'
    for root, _, files in os.walk(root_folder_path):
        for file in files:
            if file.endswith(extensions):
                yield os.path.join(root, file)


def extract_file_info_by_path(file_path: str) -> FileInfo:
    ...


def extract_image_creation_date_from_metadata(file_path: str) -> datetime:
    ...
