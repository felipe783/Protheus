from dataclasses import dataclass, field
from uuid import UUID, uuid4

class DocumentUUID:
    def __init__(self, uuid_str: str):
        self.uuid = UUID(uuid_str)