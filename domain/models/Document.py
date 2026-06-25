from datetime import datetime
from dataclasses import dataclass
from Protheus.domain.models import DocumentUUID


@dataclass
class Document:
    id: str
    created_in: datetime
    description: dict

    def toDomain(self):
        return Document(
            id=DocumentUUID(self.id),
            created_in=self.created_in,
            description=self.description
        )

    @classmethod
    def fromDomain(cls, document):
        return cls(
            id=str(document.id.uuid),
            created_in=document.created_in,
            description=document.description
        )
    