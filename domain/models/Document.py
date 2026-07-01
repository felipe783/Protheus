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