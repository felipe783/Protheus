from __future__ import annotations
import json
from Protheus.core.db_path_config import *
from Protheus.core.log_config import *

DB_PATH.parent.mkdir(parents=True, exist_ok=True)

def _get_db() -> dict:
    if not DB_PATH.exists():
        return {"documents": []}
    with open(DB_PATH, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {"documents": []}
        
def _save_db(data: dict) -> None:
    try:  
        with open(DB_PATH, "w" , encoding="utf-8") as f:
            json.dump(data,f, ensure_ascii=False, indent=2, default=str)
        logging.info(f"Salvo com sucesso -- Registro:{len(data)}")

    except Exception as e:
        logging.error(f"Erro ao salvar o banco de dados: {e}")
        raise


