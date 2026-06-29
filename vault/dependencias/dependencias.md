# Dependencias

Nao foi encontrado `requirements.txt` nem `pyproject.toml`. As dependencias abaixo foram inferidas por imports.

## Dependencias externas

### Runtime

- `fastapi`: API HTTP e upload de arquivos.
- `uvicorn`: servidor ASGI indicado no comentario de `api/main.py`.
- `pypdf`: leitura de PDF em `PdfReader.py`.
- `python-docx`: leitura de DOCX em `DocxReader.py`.
- `odfpy`: leitura de ODT em `OdtReader.py`.

### Testes

- `pytest`: testes em `test/test_db.py` e `test/test_log.py`.

## Dependencias internas

### API -> Application

`ControllerDocument.py` depende de:

- `DocumentExtractor`;
- `DocumentTypeDetector`;
- `DocumentExtensionDetector`;
- `DocumentInput`.

### Application -> Core/Domain

- `DocumentTypeDetector` usa `KEY_WORDS`.
- `DocumentExtractor` usa `DOCUMENT_PATTERNS`.
- detectores usam enums de `domain.models`.

### Domain -> Infrastructure

`FileReaderFactory.py` importa leitores concretos de infraestrutura. Isso funciona, mas inverte a dependencia esperada em Clean Architecture.

### Infrastructure -> Domain

Leitores implementam `FileReader`.

Repositorio JSON usa `Document` e `DocumentEntity`.

## Dependencias da biblioteca padrao

- `datetime`;
- `pathlib`;
- `re`;
- `json`;
- `logging`;
- `abc`;
- `enum`;
- `dataclasses`;
- `uuid`.

