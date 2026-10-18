from dataclasses import dataclass
from datetime import datetime
from domain.models.Document import Document
from domain.models.DocumentUUID import DocumentUUID
from domain.models.DocumentType import documentType
from domain.models.DocumentExtension import documentExtension

@dataclass
class DocumentEntity:
    id: str
    created_in: datetime
    description: dict
    type: documentType
    extension: documentExtension

    def toDomain(self) -> Document:
        return Document(
            id=DocumentUUID(self.id),
            created_in=self.created_in,
            description=self.description,
            type=self.type,
            extension=self.extension
        )

    @classmethod
    def fromDomain(cls, document: Document):
        return cls(
            id=str(document.id.uuid),
            created_in=document.created_in,
            description=document.description,
            type= document.type,
            extension= document.extension
        )