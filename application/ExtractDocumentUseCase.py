from application.DocumentExtensionDetector import DocumentExtensionDetector
from application.DocumentTypeDetector import DocumentTypeDetector
from application.DocumentExtractor import DocumentExtractor
from application.input.DocumentInput import DocumentInput
from domain.interfaces.DocumentRepository import DocumentRepository
from domain.models.Document import Document
from domain.models.DocumentUUID import DocumentUUID
from domain.models.FileReaderFactory import FileReaderFactory

from datetime import datetime
import tempfile
import os
import logging

class ExtractDocumentUseCase:

    def __init__(self, repository: DocumentRepository):
        self.repository = repository

    def execute(
        self,
        file_content: bytes,
        filename: str
    ) -> dict:

        extension = DocumentExtensionDetector.detect(filename)

        # Os readers recebem um caminho, então o upload vira um arquivo temporário
        with tempfile.NamedTemporaryFile(delete=False, suffix=extension.value) as tmp:
            tmp.write(file_content)
            tmp_path = tmp.name

        try:
            reader = FileReaderFactory.get(extension)
            content = reader.extract(tmp_path)
        finally: # Apaga o Arquivo Temp
            os.unlink(tmp_path)

        document_type = DocumentTypeDetector.detect(
            content=content,
            extension=extension
        )
        documentInput = DocumentInput(
            created_in=datetime.now(),
            type=document_type,
            extension=extension
        )
        extracted_data = DocumentExtractor.extract(
            content=content,
            document_type=documentInput.type
        )

        document = Document(
            id=DocumentUUID.generate(),
            created_in=documentInput.created_in,
            description=extracted_data,
            type=documentInput.type,
            extension=documentInput.extension
        )
        logging.debug(document)
        self.repository.save(document)

        return extracted_data
