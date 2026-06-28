from dataclasses import dataclass
from datetime import datetime
from models.DocumentUUID import id
from models.DocumentType import documentType
from models.DocumentExtension import documentExtension

@dataclass
class Document:
    id: id
    created_in: datetime
    description: dict
    type: documentType
    extension: documentExtension