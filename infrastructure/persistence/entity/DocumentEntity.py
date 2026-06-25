from dataclasses import dataclass
from datetime import datetime
from Protheus.domain.models import Document, DocumentUUID

@dataclass
class DocumentEntity:
    id: str
    created_in: datetime
    description: dict

    def toDomain(self) -> Document:
        return Document(
            id=DocumentUUID(self.id),
            created_in=self.created_in,
            description=self.description
        )

    @classmethod
    def fromDomain(cls, document: Document):
        return cls(
            id=str(document.id.uuid),
            created_in=document.created_in,
            description=document.description
        )