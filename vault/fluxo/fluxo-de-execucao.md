# Fluxo de Execucao

Existem dois fluxos importantes:

- [[fluxo/fluxo-http-atual]]: o que a rota FastAPI executa hoje.
- [[fluxo/fluxo-caso-de-uso-pretendido]]: o fluxo sugerido pelo caso de uso `ExtractDocumentUseCase`.

## Start da aplicacao

1. O comando `python -m uvicorn api.main:app --reload` carrega `api/main.py`.
2. `api/main.py` cria `FastAPI()`.
3. `api/main.py` registra `documentController`.
4. FastAPI expoe a rota `POST /document/extract`.
5. Cliente envia arquivo via multipart upload.
6. A rota processa o arquivo e retorna um dicionario de campos extraidos.

## Fim do fluxo

No fluxo HTTP atual, o fim e a resposta JSON retornada diretamente pela rota. Nao ha persistencia automatica do documento no banco JSON.

Persistencia existe em [[modulos/infrastructure]], mas nao esta ligada ao endpoint atual.

