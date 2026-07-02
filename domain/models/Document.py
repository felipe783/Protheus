from dataclasses import dataclass
from datetime import datetime
from domain.models.DocumentUUID import DocumentUUID
from domain.models.DocumentType import documentType
from domain.models.DocumentExtension import documentExtension

@dataclass
class Document:
    id: DocumentUUID
    created_in: datetime
    description: dict[str, str | None]
    type: documentType
    extension: documentExtension

    def __str__(self):
        return (
            f"\nDocument(\n"
            f"  id={self.id},\n"
            f"  created_in={self.created_in},\n"
            f"  description={self.description},\n"
            f"  type={self.type},\n"
            f"  extension={self.extension}\n"
            f")"
        )