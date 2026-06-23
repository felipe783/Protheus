from api.routers.deps import _get_db, _save_db
from Protheus.domain.models.documentModel import Documento

class JSONDocumentPersistence:

    def __init__(self):
        self._data = _get_db()

    def add(self, documento: Documento) -> Documento:
        self._data["documentos"].append(documento.__dict__)
        _save_db(self._data)
        return documento