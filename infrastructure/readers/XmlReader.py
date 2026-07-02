from pathlib import Path
from domain.interfaces.FileReader import FileReader

class XmlReader(FileReader):

    def extract(self, path: str) -> str:
        with open(path, "rb") as f:
            raw = f.read()
        try:
            return raw.decode("utf-8")
        except UnicodeDecodeError:
            return raw.decode("latin-1", errors="ignore")