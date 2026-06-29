# Modulo API

O modulo `api` e a borda HTTP do sistema.

## Arquivos

### `api/main.py`

Responsabilidades:

- criar `app = FastAPI()`;
- importar `documentController`;
- registrar o router com `app.include_router(documentController)`.

Entrypoint de execucao:

```powershell
python -m uvicorn api.main:app --reload
```

Documentacao interativa esperada:

```text
http://127.0.0.1:8000/docs
```

### `api/routers/ControllerDocument.py`

Define o router:

```python
documentController = APIRouter(
    prefix="/document",
    tags=["document"]
)
```

Endpoint principal:

```text
POST /document/extract
```

Responsabilidades atuais:

- receber um arquivo via multipart upload;
- ler bytes com `await file.read()`;
- decodificar conteudo como UTF-8;
- detectar extensao;
- detectar tipo documental;
- extrair campos;
- retornar os dados extraidos.

Detalhes da rota em [[api/api-e-rotas]].

## Comunicacao

`ControllerDocument.py` chama diretamente componentes de [[modulos/application]]:

- `DocumentExtensionDetector`;
- `DocumentTypeDetector`;
- `DocumentExtractor`;
- `DocumentInput`.

Essa comunicacao direta funciona, mas deixa parte da orquestracao na API. O desenho mais limpo seria delegar para `ExtractDocumentUseCase`. Ver [[arquitetura/observacoes-tecnicas]].

