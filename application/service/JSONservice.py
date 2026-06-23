from datetime import datetime
import uuid
from Protheus.domain.interfaces.documentRepository import DocumentoRepository
from Protheus.domain.models.documentModel import Documento

class DocumentoService:
    def __init__(self, repo: DocumentoRepository):
        self.repo = repo

    def criar_documento(self, dados: dict):
        doc = Documento(
            id=str(uuid.uuid4()),
            criado_em=datetime.utcnow(),
            dados=dados
        )
        return self.repo.add(doc)