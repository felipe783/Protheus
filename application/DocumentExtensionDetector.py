from pathlib import Path
from domain.models.DocumentExtension import documentExtension

class DocumentExtensionDetector:
    @staticmethod
    def detect(file_path: str) -> documentExtension:

        extension = Path(file_path).suffix.lower()

        match extension:
            case ".pdf":
                return documentExtension.PDF

            case ".xml":
                return documentExtension.XML

            case ".docx":
                return documentExtension.DOCX

            case ".odt":
                return documentExtension.ODT

            case _:
                raise ValueError(
                    f"Extensão não suportada: {extension}"
                )