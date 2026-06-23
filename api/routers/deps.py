from __future__ import annotations
import json
from core.db_path_config import *
from core.log_config import *

DB_PATH.parent.mkdir(parents=True, exist_ok=True)

def _get_db() -> dict:
    if not DB_PATH.exists():
        logging.warning("DB não encontrado. Retornando estrutura vazia.")
        return {"documents": []}

    try:
        with open(DB_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)

        # validação
        if not isinstance(data, dict):
            logging.warning("DB inválido (não é dict). Usando fallback.")
            return {"documents": []}

        if "documents" not in data:
            logging.warning("DB sem chave 'documents'. Usando fallback.")
            return {"documents": []}

        logging.info(f"DB carregado com sucesso. Registros: {len(data.get('documents', []))}")
        return data

    except json.JSONDecodeError:
        logging.error("DB corrompido (JSON inválido). Usando fallback.")
        return {"documents": []}

    except Exception as e:
        logging.error(f"Erro inesperado ao ler DB: {e}")
        return {"documents": []}
        
def _save_db(data: dict) -> None:
    try:  
        with open(DB_PATH, "w" , encoding="utf-8") as f:
            json.dump(data,f, ensure_ascii=False, indent=2, default=str)
        logging.info(f"Salvo com sucesso -- Registro:{len(data)}")

    except Exception as e:
        logging.error(f"Erro ao salvar o banco de dados: {e}")
        raise


