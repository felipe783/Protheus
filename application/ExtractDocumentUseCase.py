from application.DocumentExtensionDetector import DocumentExtensionDetector
from application.DocumentTypeDetector import DocumentTypeDetector
from application.DocumentExtractor import DocumentExtractor
from domain.models.FileReaderFactory import FileReaderFactory

class ExtractDocumentUseCase:

    def execute(
        self,
        file_content: bytes,
        filename: str
    ) -> dict:

        extension = DocumentExtensionDetector.detect(filename)
        reader = FileReaderFactory.create(extension)
        content = reader.read(file_content)
        
        document_type = DocumentTypeDetector.detect(
            content=content,
            extension=extension
        )

        extracted_data = DocumentExtractor.extract(
            content=content,
            document_type=document_type
        )

        return {
            "document_type": document_type,
            "data": extracted_data
        }