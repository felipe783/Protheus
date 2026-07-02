from __future__ import annotations
import json
from pathlib import Path

DB_PATH = Path("infrastructure/db/db.json")

def get_db() -> dict:
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
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(DB_PATH, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4, default=str)