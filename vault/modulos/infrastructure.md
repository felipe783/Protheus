# Modulo Infrastructure

O modulo `infrastructure` contem detalhes tecnicos: leitura de arquivos, persistencia e logs.

## Readers

### `PdfReader.py`

Usa `pypdf.PdfReader` para extrair texto pagina por pagina.

Contrato implementado:

```python
extract(path: str) -> str
```

### `XmlReader.py`

Usa `Path(path).read_text(encoding="utf-8", errors="ignore")`.

### `DocxReader.py`

Usa `python-docx`:

```python
from docx import Document
```

Extrai os parágrafos e junta com `\n`.

### `OdtReader.py`

Usa `odfpy`:

```python
from odf import text, teletype
from odf.opendocument import load
```

Extrai texto de parágrafos ODT.

## Persistencia

### `infrastructure/db/db.json`

Banco JSON local:

```json
{
  "documents": []
}
```

### `JsonRepositoryDeps.py`

Funcoes:

- `get_db()`;
- `save_db(data)`.

Responsabilidades:

- criar diretorio do banco se necessario;
- carregar JSON;
- tolerar arquivo ausente;
- tolerar JSON invalido;
- salvar JSON indentado.

### `JsonDocumentRepository.py`

Repositorio concreto para `Document`.

Metodos:

- `save(document)`;
- `getAll()`.

Usa `DocumentEntity` para converter entre dominio e persistencia.

### `DocumentEntity.py`

Entidade de persistencia com:

- `toDomain()`;
- `fromDomain()`.

## Logs

`infrastructure/logs/logs.log` e o arquivo de saida configurado por [[modulos/core]].

