from dataclasses import dataclass
from datetime import datetime
from models.DocumentUUID import id


@dataclass
class Document:
    id: id
    created_in: datetime
    description: dict