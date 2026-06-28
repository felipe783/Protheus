from pathlib import Path
from domain.interfaces.FileReader import FileReader

class XmlReader(FileReader):

    def extract(self, path: str) -> str:
        return Path(path).read_text(
            encoding="utf-8",
            errors="ignore"
        )