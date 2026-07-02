from domain.models.Document import Document
from domain.models.DocumentUUID import DocumentUUID
from domain.models.FileReaderFactory import FileReaderFactory 
from infrastructure.persistence.entity.DocumentEntity import DocumentEntity
from infrastructure.persistence.repository.JsonRepositoryDeps import get_db, save_db
from application.DocumentExtractor import DocumentExtractor
from application.DocumentTypeDetector import DocumentTypeDetector
from application.DocumentExtensionDetector import DocumentExtensionDetector
from application.input.DocumentInput import DocumentInput
from core.Logs.LogUploadConfig import logging
from fastapi import APIRouter, UploadFile, File

from datetime import datetime
import tempfile
import os
import logging

documentController = APIRouter(
    prefix="/document",
    tags=["document"]
)

@documentController.post("/extract")
async def extract_document(file: UploadFile = File(...)):

    content = await file.read()
    extension = DocumentExtensionDetector.detect(file.filename)

    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{extension.value}") as tmp:
        tmp.write(content)
        tmp_path = tmp.name

    # Chamando a factory
    try:
        reader = FileReaderFactory.get(extension)
        text = reader.extract(tmp_path)
        #logging.debug(f"Texto extraído de {file.filename}:\n{text}")
    finally: # Fecha o Arquivo Temp
        os.unlink(tmp_path)

    documentType = DocumentTypeDetector.detect(content=text,extension=extension)
    #logging.debug(f"Tipo documento Detectado {documentType}")
    documentInput = DocumentInput(
        created_in=datetime.now(),
        type=documentType,
        extension=extension
    )
    result = DocumentExtractor.extract(content=text,document_type=documentInput.type)

    document = Document(
        id=DocumentUUID.generate(), 
        created_in=documentInput.created_in,
        description=result,
        type=documentInput.type,
        extension=documentInput.extension
    )
    logging.debug(document)
    # Salvar no JSON
    entity = DocumentEntity.fromDomain(document) # Converter do dominio -> Json
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