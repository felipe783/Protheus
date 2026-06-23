# app/api/deps.py

"""
Dependências específicas do sistema de processamento de documentos
(CRLV-e, Cartão CNPJ, DANFE/XML, laudos laboratoriais e contratos).
"""

from enum import Enum
from typing import Generator, Optional
from fastapi import Depends, HTTPException, UploadFile, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from Protheus.core.db_path_config import settings
from Protheus.infrastructure.db.session import SessionLocal
from Protheus.app.domain.models.user import User
from Protheus.app.infrastructure.repositories.user_repository import UserRepository
from Protheus.app.infrastructure.repositories.checklist_repository import ChecklistRepository
from Protheus.application.services.ocr_service import OCRService
from Protheus.application.services.document_classifier import DocumentClassifierService
from Protheus.application.services.nfe_parser import NFeParserService
from Protheus.application.services.embedding_service import EmbeddingService
from Protheus.application.services.ner_service import NERService
from Protheus.application.services.storage_service import StorageService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

# Banco de dados

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Autenticação / Autorização

class UserRole(str, Enum):
    OPERADOR = "operador"   # faz upload, vê extrações (RF01, RF12)
    JURIDICO = "juridico"   # mantém checklist (RF13), revisa contratos
    ADMIN = "admin"


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: Optional[str] = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = UserRepository(db).get_by_id(user_id)
    if user is None:
        raise credentials_exception
    return user


def require_role(*allowed_roles: UserRole):
    """
    Factory de dependência: restringe uma rota a determinados papéis.
    Usada na rota de manutenção da checklist (RF13), que só o time
    jurídico pode editar.
    """
    def dependency(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in [r.value for r in allowed_roles]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Permissão insuficiente para esta operação",
            )
        return current_user
    return dependency

# RF01 — Validação do upload (extensão / content-type)

ALLOWED_EXTENSIONS = {".pdf", ".xml", ".docx", ".odt"}
ALLOWED_CONTENT_TYPES = {
    "application/pdf",
    "text/xml",
    "application/xml",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "application/vnd.oasis.opendocument.text",
}

async def validate_uploaded_file(file: UploadFile) -> UploadFile:
    """
    Garante que o arquivo é de um formato suportado (RF01).
    A *classificação do tipo de documento* (CRLV-e, CNPJ, DANFE,
    laudo, contrato) é responsabilidade do DocumentClassifierService
    (RF03), não desta função — aqui só filtramos formato de arquivo.
    """
    extension = "." + file.filename.rsplit(".", 1)[-1].lower() if "." in file.filename else ""

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=f"Extensão '{extension}' não suportada. Use: {', '.join(ALLOWED_EXTENSIONS)}",
        )

    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=f"Content-Type '{file.content_type}' não suportado",
        )

    return file

# Serviços de domínio (RF03 a RF09)

def get_storage_service() -> StorageService:
    """Abstrai onde o arquivo fica salvo (disco local, S3, etc)."""
    return StorageService(bucket=settings.STORAGE_BUCKET)


def get_ocr_service() -> OCRService:
    """
    
    """
    return OCRService(engine=settings.OCR_ENGINE)


def get_document_classifier(
    ocr: OCRService = Depends(get_ocr_service),
) -> DocumentClassifierService:
    """
    RF03 — decide o tipo de documento a partir da extensão e de
    palavras-chave no texto extraído (recorre ao OCR quando o PDF
    não tem texto nativo).
    """
    return DocumentClassifierService(ocr_service=ocr)


def get_nfe_parser(
    ocr: OCRService = Depends(get_ocr_service),
) -> NFeParserService:
    """RF04 — parsing de <ide>/<dest>/<det>/<total> com fallback para OCR."""
    return NFeParserService(ocr_service=ocr)


def get_embedding_service() -> EmbeddingService:
    """
    RF08 — embeddings para comparação semântica entre cláusulas do
    contrato segmentado e a checklist obrigatória.
    """
    return EmbeddingService(
        model_name=settings.EMBEDDING_MODEL,
        similarity_threshold=settings.CLAUSE_SIMILARITY_THRESHOLD,
    )


def get_ner_service() -> NERService:
    """RF09 — reconhecimento de entidades (partes, valores, prazos)."""
    return NERService(model_name=settings.NER_MODEL)


def get_checklist_repository(db: Session = Depends(get_db)) -> ChecklistRepository:
    """
    RF13 — a checklist fica em banco (não em código), justamente
    para o time jurídico poder editá-la sem deploy nem retraining.
    """
    return ChecklistRepository(db)

# Paginação (usada nas filas de revisão humana — RF12)

class PaginationParams:
    def __init__(self, skip: int = 0, limit: int = 50):
        self.skip = skip
        self.limit = min(limit, 100)