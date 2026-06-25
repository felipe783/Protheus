import pytest
from Protheus.infrastructure.persistence.repository.JsonRepositoryDeps import _get_db, _save_db
# python -m pytest -v

def test_get_db_file_not_exists(tmp_path, monkeypatch):
    fake_db = tmp_path / "db.json"
    monkeypatch.setattr("core.dbPathConfig.DB_PATH", fake_db)
    result = _get_db()
    assert result == {"documents": []}

def test_save_and_get_db(tmp_path, monkeypatch):
    fake_db = tmp_path / "db.json"
    monkeypatch.setattr("core.dbPathConfig.DB_PATH", fake_db)
    data = {
        "documents": [
            {"id": 1, "name": "teste"}
        ]
    }

    _save_db(data)
    result = _get_db()
    assert result == data

def test_get_db_corrupt_file(tmp_path, monkeypatch):
    fake_db = tmp_path / "db.json"
    fake_db.write_text("isso nao e json", encoding="utf-8")

    monkeypatch.setattr("core.dbPathConfig.DB_PATH", fake_db)

    result = _get_db()

    assert result == {"documents": []}