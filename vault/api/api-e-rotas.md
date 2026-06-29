# APIs e Rotas

## FastAPI

O objeto `app` e criado em:

```text
api/main.py
```

Comando sugerido no proprio codigo:

```powershell
python -m uvicorn api.main:app --reload
```

Swagger/OpenAPI:

```text
http://127.0.0.1:8000/docs
```

## Router de documentos

Arquivo:

```text
api/routers/ControllerDocument.py
```

Router:

```python
documentController = APIRouter(
    prefix="/document",
    tags=["document"]
)
```

## `POST /document/extract`

Entrada:

- `file: UploadFile = File(...)`

Processamento:

- le o arquivo;
- decodifica como texto;
- detecta extensao;
- detecta tipo documental;
- extrai campos por regex.

Saida:

- `dict` com campos extraidos;
- campos sem match retornam `None`;
- se nao houver padroes para o tipo, retorna `{}`.

## Classes/funcoes chamadas

- `DocumentExtensionDetector.detect`
- `DocumentTypeDetector.detect`
- `DocumentInput`
- `DocumentExtractor.extract`

## Relacao com fluxo

Ver [[fluxo/fluxo-http-atual]].

