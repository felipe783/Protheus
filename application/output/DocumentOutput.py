from dataclasses import dataclass
from datetime import datetime

from domain.models.DocumentType import documentType
from domain.models.DocumentExtension import documentExtension
from domain.models.Document import Document


@dataclass(frozen=True)
class DocumentOutput:
    id: str
    created_in: datetime
    description: dict[str, str | None]
    type: documentType
    extension: documentExtension

    @classmethod
    def fromDocument(cls, document: Document):
        return cls(
            id=str(document.id.uuid),
            created_in=document.created_in,
            description=document.description,
            type=document.type,
            extension=document.extension
        )