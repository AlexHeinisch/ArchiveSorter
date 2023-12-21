from datetime import datetime
from typing import Generator
import os
from archivesorter.database.models import FileInfo
import hashlib


def get_all_file_paths_by_root_folder(
    root_folder_path: str,
) -> Generator[str, None, None]:
    extensions = '*'
    for root, _, files in os.walk(root_folder_path):
        for file in files:
            if extensions == '*' or file.endswith(extensions):
                yield os.path.join(root, file)


def extract_file_info_by_path(file_path: str) -> FileInfo:
    creation_date = datetime.fromtimestamp(os.path.getctime(file_path))
    modified_date = datetime.fromtimestamp(os.path.getmtime(file_path))
    file_content_hash = hash_file_content(file_path)
    return FileInfo(
        source_path=file_path,
        file_last_modified=modified_date,
        file_created=creation_date,
        file_hash=file_content_hash,
        photo_created=None,
        evaluated_datetime=None,
        evaluated_category=None,
        computed_target_path=None,
    )


def hash_file_content(file_path: str) -> str:
    sha256_hash = hashlib.sha3_256()
    with open(file_path, 'rb') as file:
        for chunk in iter(lambda: file.read(4096), b''):
            sha256_hash.update(chunk)
    return sha256_hash.hexdigest()


def extract_image_creation_date_from_metadata(file_path: str) -> datetime:
    ...
