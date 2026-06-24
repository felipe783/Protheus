from __future__ import annotations
import json
import core.db_path_config as db_config
import core.log_config as log_config

db_config.DB_PATH.parent.mkdir(parents=True, exist_ok=True)

def _get_db() -> dict:
    if not db_config.DB_PATH.exists():
        log_config.logging.warning("DB não encontrado. Retornando estrutura vazia.")
        return {"documents": []}

    try:
        with open(db_config.DB_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)

        # validação
        if not isinstance(data, dict):
            log_config.logging.warning("DB inválido (não é dict). Usando fallback.")
            return {"documents": []}

        if "documents" not in data:
            log_config.logging.warning("DB sem chave 'documents'. Usando fallback.")
            return {"documents": []}

        log_config.logging.info(f"DB carregado com sucesso. Registros: {len(data.get('documents', []))}")
        return data

    except json.JSONDecodeError:
        log_config.logging.error("DB corrompido (JSON inválido). Usando fallback.")
        return {"documents": []}

    except Exception as e:
        log_config.logging.error(f"Erro inesperado ao ler DB: {e}")
        return {"documents": []}
        
def _save_db(data: dict) -> None:
    try:  
        with open(db_config.DB_PATH, "w" , encoding="utf-8") as f:
            json.dump(data,f, ensure_ascii=False, indent=2, default=str)
        log_config.logging.info(f"Salvo com sucesso -- Registro:{len(data)}")

    except Exception as e:
        log_config.logging.error(f"Erro ao salvar o banco de dados: {e}")
        raise