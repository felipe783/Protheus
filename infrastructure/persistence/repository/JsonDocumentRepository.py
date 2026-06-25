from domain.models import Document
from domain.interfaces import DocumentRepository
from infrastructure.persistence.entity import DocumentEntity

class JsonDocumentRepository(DocumentRepository):

    def __init__(self, documentEntityRepository):
        self._documentEntityRepository = documentEntityRepository

    def save(self, document: Document) -> Document:
        entity = DocumentEntity.fromDomain(document)

        return self._documentEntityRepository.save(entity).toDomain()

