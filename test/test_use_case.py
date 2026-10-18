from pathlib import Path
from application.ExtractDocumentUseCase import ExtractDocumentUseCase
from infrastructure.persistence.repository.JsonDocumentRepository import JsonDocumentRepository
from infrastructure.persistence.repository.JsonRepositoryDeps import get_db

def test_execute_returns_fields_and_saves(tmp_path, monkeypatch):
    fake_db = tmp_path / "db.json"
    monkeypatch.setattr("core.dbPathConfig.DB_PATH", fake_db)

    content = (Path(__file__).resolve().parent.parent / "test.xml").read_bytes()
    result = ExtractDocumentUseCase(JsonDocumentRepository()).execute(content, "test.xml")

    saved = get_db()["documents"]
    assert len(saved) == 1
    assert saved[0]["description"] == result
    assert result["cnpj_emitente"] == "99999090910270"
    # Mesmo formato que o controller gravava antes: enums como texto
    assert saved[0]["type"] == "danfe_xml"
    assert saved[0]["extension"] == ".xml"
