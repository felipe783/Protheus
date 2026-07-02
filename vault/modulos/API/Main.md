# Modulo main

O modulo `main` e a borda HTTP do sistema.
## Arquivo

### `api/main.py`

Responsabilidades:
- criar `app = FastAPI()`;
- Permitir Requisições HTTP de origens definidas 
- registrar o "Router" com `app.include_router(documentController)`.

```python
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(documentController)
```

Endpoint principal:

```text
POST /document/extract
```
## Comunicação

`main.py` chama diretamente o componente de [[Controller]] e com isso nele é chamado:

- `DocumentExtensionDetector`;
- `DocumentTypeDetector`;
- `DocumentExtractor`;
- `DocumentInput`.

