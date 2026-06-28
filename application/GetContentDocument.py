import re
from pathlib import Path

def getXmlContent(file_path: str) -> str:
    return Path(file_path).read_text(
        encoding="utf-8",
        errors="ignore"
    )