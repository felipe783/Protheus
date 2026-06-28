from pathlib import Path
from fastapi import UploadFile

def getExtension(file: UploadFile) -> str:
    return Path(file.filename).suffix.lower()