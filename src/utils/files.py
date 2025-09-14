import os
import uuid
from pathlib import Path
import shutil

DOWNLOAD_DIR = os.getenv("DOWNLOAD_DIR")

def place_for_download() -> str:
    download_path = os.path.join(DOWNLOAD_DIR, f"downloads{uuid.uuid4()}")
    os.makedirs(download_path, exist_ok=True)
    return download_path

def zip(folder_path: str):
    zip_filename = os.path.join(DOWNLOAD_DIR, f"spotiDown{uuid.uuid4()}")
    shutil.make_archive(zip_filename, "zip", folder_path)
    return f"{zip_filename}.zip"