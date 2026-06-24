import datetime
from typing import Any
import uuid
from pyparsing import Optional
from Protheus.api.routers.deps import _save_db, _get_db


class JSONRepository:

    def __init__(self) -> None:
        self._data = _get_db()

    def add_documento(self, documento: dict) -> dict:
        documento["id"] = documento.get("id") or str(uuid.uuid4())
        documento["criado_em"] = documento.get("criado_em") or datetime.utcnow().isoformat()
        self._data["documentos"].append(documento)
        _save_db(self._data)
        return documento

    def get_documento(self, doc_id: str) -> Optional[dict]:
        return next((d for d in self._data["documentos"] if d["id"] == doc_id), None)

    def list_documentos(self) -> list[dict]:
        return self._data["documentos"]

    def update_documento(self, doc_id: str, **campos: Any) -> Optional[dict]:
        doc = self.get_documento(doc_id)
        if doc:
            doc.update(campos)
            _save_db(self._data)
        return doc
