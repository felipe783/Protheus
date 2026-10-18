from __future__ import annotations
import json
import logging
from core import dbPathConfig

def get_db() -> dict:
    # Lido a cada chamada para que o monkeypatch de core.dbPathConfig.DB_PATH funcione
    DB_PATH = dbPathConfig.DB_PATH
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    if not DB_PATH.exists():
        return {"documents": []}
    try:
        with open(DB_PATH, "r", encoding="utf-8") as file:
            data = json.load(file)
        if not isinstance(data, dict):
            return {"documents": []}
        data.setdefault("documents", [])
        return data
    
    except (json.JSONDecodeError, Exception):
        return {"documents": []}

def save_db(data: dict) -> None:
    DB_PATH = dbPathConfig.DB_PATH
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(DB_PATH, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4, default=str)
    logging.info(f"Salvo com sucesso em {DB_PATH}")
