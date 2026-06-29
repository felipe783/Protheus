# Observacoes Tecnicas

Esta nota lista divergencias e riscos encontrados durante a analise.

## Rota atual nao usa o caso de uso

`api/routers/ControllerDocument.py` chama diretamente:

- `DocumentExtensionDetector`;
- `DocumentTypeDetector`;
- `DocumentExtractor`.

O arquivo `application/ExtractDocumentUseCase.py` existe, mas nao e usado pela rota atual.

Impacto: a camada API contem orquestracao que poderia estar na camada [[modulos/application]].

## Leitores usam `extract`, caso de uso chama `read`

Os leitores em `infrastructure/readers` implementam:

```python
extract(self, path: str) -> str
```

Mas `ExtractDocumentUseCase.execute` chama:

```python
reader.read(file_content)
```

Impacto: o caso de uso pretendido tende a quebrar se executado como esta.

## Rota decodifica tudo como UTF-8

`ControllerDocument.py` faz:

```python
text = content.decode("utf-8", errors="ignore")
```

Isso funciona melhor para XML/texto. Para PDF, DOCX e ODT, a extracao correta deveria passar pelos leitores especificos.

## Imports possivelmente quebrados

`domain/models/Document.py` importa de `models.*`, mas o pacote real esta em `domain.models.*`.

`DocumentEntity.py` importa `from domain.models import Document, DocumentUUID, DocumentType, DocumentExtension`, o que pode retornar modulos em vez de classes se nao houver `__init__.py` exportando corretamente.

## Testes usam monkeypatch em path diferente

Os testes alteram `core.dbPathConfig.DB_PATH`, mas `JsonRepositoryDeps.py` usa seu proprio `DB_PATH = Path("infrastructure/db/db.json")`.

Impacto: os testes podem nao isolar o banco real como esperado.

## Dependencias sem manifesto

Nao foi encontrado `requirements.txt` ou `pyproject.toml`. As dependencias foram inferidas por imports. Veja [[dependencias/dependencias]].

