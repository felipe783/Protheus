from pathlib import Path
from domain.models.DocumentExtension import documentExtension


class DocumentExtensionDetector:
    @staticmethod
    def detect(filename: str) -> documentExtension:
        extension = Path(filename).suffix.lower()

        try:
            return documentExtension(extension)
        except ValueError:
            raise ValueError(
                f"Extensão não suportada: {extension}"
            )