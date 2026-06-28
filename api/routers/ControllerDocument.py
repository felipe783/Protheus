from datetime import datetime
from fastapi import APIRouter, UploadFile, File
from application.ExtractDocumentUseCase import DocumentExtractor
from application.DocumentTypeDetector import DocumentTypeDetector
from application.DocumentExtensionDetector import DocumentExtensionDetector
from application.input.DocumentInput import DocumentInput

documentController = APIRouter(
    prefix="/document",
    tags=["document"]
)

@documentController.post("/extract")
async def extract_document(
    file: UploadFile = File(...)
):
    content = await file.read()

    extension = DocumentExtensionDetector.detect(file.filename)

    document_type = DocumentTypeDetector.detect(
        content=content.decode("utf-8", errors="ignore"),
        extension=extension
    )

    document_input = DocumentInput(
        created_in=datetime.now(),
        type=document_type,
        extension=extension
    )

    result = DocumentExtractor().execute(
        file_content=content,
        document_input=document_input
    )

    return result