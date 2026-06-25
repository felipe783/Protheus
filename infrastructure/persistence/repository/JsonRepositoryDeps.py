from __future__ import annotations

import json
import logging
from pathlib import Path

DB_PATH = Path("infrastructure/db/db.json")

def get_db() -> dict:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    if not DB_PATH.exists():
        logging.warning("DB não encontrado. Retornando estrutura vazia.")
        return {"documents": []}

    try:
        with open(DB_PATH, "r", encoding="utf-8") as file:
            data = json.load(file)

        if not isinstance(data, dict):
            logging.warning("DB inválido. Usando estrutura padrão.")
            return {"documents": []}
        data.setdefault("documents", [])
        logging.info(
            "DB carregado com sucesso. Registros: %s",
            len(data["documents"])
        )
        return data
    
    except json.JSONDecodeError:
        logging.error("JSON inválido. Usando estrutura padrão.")
        return {"documents": []}
    except Exception as error:
        logging.error("Erro ao carregar DB: %s", error)
        return {"documents": []}

def save_db(data: dict) -> None:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    try:
        with open(DB_PATH, "w", encoding="utf-8") as file:
            json.dump(
                data,
                file,
                ensure_ascii=False,
                indent=4,
                default=str
            )
        logging.info(
            "DB salvo com sucesso. Registros: %s",
            len(data.get("documents", []))
        )

    except Exception as error:
        logging.error("Erro ao salvar DB: %s", error)
        raise