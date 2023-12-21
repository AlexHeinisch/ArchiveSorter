from datetime import datetime
from PIL import Image
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


image_extensions = [
    '.jpg',
    '.jpeg',
    '.jpe',
    '.jfif',
    '.tiff',
    '.tif',
    '.raw',
    '.nef',
    '.cr2',
    '.png',
    '.gif',
    '.bmp',
]


def extract_image_creation_date_from_metadata_if_image(
    file_path: str,
) -> datetime | None:
    if not any([file_path.endswith(ext) for ext in image_extensions]):
        return None
    try:
        # Open the image file
        with Image.open(file_path) as img:
            # Get the EXIF data
            exif_data = img.getexif()

            # If the image has EXIF data
            if exif_data is not None:
                date = exif_data.get(36867) or exif_data.get(306)
                return datetime.strptime(date, '%Y:%m:%d %H:%M:%S') if date else None
            else:
                print('No EXIF data found in the image.')
    except FileNotFoundError:
        print(f'File not found: {file_path}')
    except Exception as e:
        print(f'Error extracting EXIF data: {e}')
