from Protheus.infrastructure.persistence.repository.JsonRepositoryDeps import _save_db

def test_save_logs(tmp_path, monkeypatch, caplog):
    fake_db = tmp_path / "db.json"
    monkeypatch.setattr("core.dbPathConfig.DB_PATH", fake_db)

    data = {"documents": []}

    with caplog.at_level("INFO"):
        _save_db(data)

    assert "Salvo com sucesso" in caplog.text