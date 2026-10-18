from application.ExtractDocumentUseCase import ExtractDocumentUseCase
from infrastructure.persistence.repository.JsonDocumentRepository import JsonDocumentRepository
import core.Logs.LogUploadConfig  # noqa: F401 - o import executa o logging.basicConfig
from fastapi import APIRouter, UploadFile, File

documentController = APIRouter(
    prefix="/document",
    tags=["document"]
)

@documentController.post("/extract")
async def extract_document(file: UploadFile = File(...)):

    content = await file.read()
    # A API escolhe a implementação do repositório; a application só conhece a interface
    useCase = ExtractDocumentUseCase(JsonDocumentRepository())
    return useCase.execute(file_content=content, filename=file.filename)
