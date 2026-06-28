from dataclasses import dataclass
from datetime import datetime
from domain.models.DocumentType import documentType
from domain.models.DocumentExtension import documentExtension

@dataclass(frozen=True)
class DocumentInput:
    created_in: datetime
    type: documentType
    extension: documentExtension

    