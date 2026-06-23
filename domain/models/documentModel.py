from dataclasses import dataclass
from datetime import datetime

@dataclass
class Documento:
    id: str
    criado_em: datetime
    dados: dict