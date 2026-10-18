from domain.models.Document import Document
from domain.interfaces.DocumentRepository import DocumentRepository
from infrastructure.persistence.entity.DocumentEntity import DocumentEntity
from infrastructure.persistence.repository.JsonRepositoryDeps import get_db,save_db

class JsonDocumentRepository(DocumentRepository):

    def save(self, document):
        data = get_db()
        data["documents"].append(DocumentEntity.fromDomain(document).__dict__)

        save_db(data)
        return document

    def getAll(self) -> list[Document]:
        data = get_db()

        return[
            DocumentEntity(**item).toDomain()
            for item in data["documents"]
            ]
