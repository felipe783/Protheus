from datetime import datetime
from domain.models.Document import Document
from domain.models.DocumentUUID import DocumentUUID
from infrastructure.persistence.entity.DocumentEntity import DocumentEntity
from infrastructure.persistence.repository.JsonRepositoryDeps import get_db, save_db
from application.DocumentExtractor import DocumentExtractor
from application.DocumentTypeDetector import DocumentTypeDetector
from application.DocumentExtensionDetector import DocumentExtensionDetector
from application.input.DocumentInput import DocumentInput
from fastapi import APIRouter, UploadFile, File


documentController = APIRouter(
    prefix="/document",
    tags=["document"]
)

@documentController.post("/extract")
async def extract_document(
    file: UploadFile = File(...)
):
    content = await file.read()
    text = content.decode("utf-8", errors="ignore")

    extension = DocumentExtensionDetector.detect(file.filename)

    documentType = DocumentTypeDetector.detect(
        content=text,
        extension=extension
    )

    documentInput = DocumentInput(
        created_in=datetime.now(),
        type=documentType,
        extension=extension
    )

    result = DocumentExtractor.extract(
        content=text,
        document_type=documentInput.type
    )

    document = Document(
        id=DocumentUUID.generate(),  # ou como você gera UUID
        created_in=documentInput.created_in,
        description=result,
        type=documentInput.type,
        extension=documentInput.extension
    )

    entity = DocumentEntity.fromDomain(document)

    db = get_db()
    db["documents"].append({
        "id": entity.id,
        "created_in": entity.created_in,
        "description": entity.description,
        "type": entity.type.value,
        "extension": entity.extension.value
    })

    save_db(db)
    return result