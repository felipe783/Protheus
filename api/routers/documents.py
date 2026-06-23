from fastapi import APIRouter, Depends, UploadFile
import deps_true  
from Protheus.app.domain.models.user import User
from Protheus.app.infrastructure.repositories.checklist_repository import ChecklistRepository
from Protheus.application.services.document_classifier import DocumentClassifierService
from Protheus.application.services.storage_service import StorageService
from Protheus.application.services.ner_service import NERService
from Protheus.application.services.embedding_service import EmbeddingService

router = APIRouter()
# upload (RF01 + RF03)
@router.post("/documents")
async def upload_document(
    file: UploadFile = Depends(deps_true.validate_uploaded_file),
    classifier: DocumentClassifierService = Depends(deps_true.get_document_classifier),
    storage: StorageService = Depends(deps_true.get_storage_service),
    current_user: User = Depends(deps_true.get_current_user),
):
    doc_type = await classifier.classify(file)   # RF03
    path = await storage.save(file)
    ...

# manutenção da checklist (RF13 — só jurídico)
@router.put("/checklist/{item_id}")
def update_checklist_item(
    item_id: int,
    checklist_repo: ChecklistRepository = Depends(deps_true.get_checklist_repository),
    _: User = Depends(deps_true.require_role(deps_true.UserRole.JURIDICO, deps_true.UserRole.ADMIN)),
):
    ...

# análise de contrato (RF02, RF07–RF09)
@router.post("/contracts/{doc_id}/analyze")
def analyze_contract(
    doc_id: int,
    embeddings: EmbeddingService = Depends(deps_true.get_embedding_service),
    ner: NERService = Depends(deps_true.get_ner_service),
    checklist_repo: ChecklistRepository = Depends(deps_true.get_checklist_repository),
):
    ...