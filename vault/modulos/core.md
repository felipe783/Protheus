# Modulo Core

O modulo `core` agrupa configuracoes e constantes transversais.

## `DocumentKeyWords.py`

Define `KEY_WORDS`, um dicionario que mapeia `documentType` para listas de palavras-chave.

Usado por:

- `application/DocumentTypeDetector.py`.

Tipos cobertos:

- CRLV-e;
- Cartao CNPJ;
- DANFE XML;
- Laudo;
- Contrato.

## `DocumentPatternsRegex.py`

Define padroes regex para extracao estruturada.

Conjuntos:

- `NFE_PATTERNS`;
- `CNPJ_PATTERNS`;
- `CRLV_PATTERNS`;
- `DOCUMENT_PATTERNS`.

Usado por:

- `application/DocumentExtractor.py`.

## `dbPathConfig.py`

Define:

```python
BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "infrastructure" / "db" / "db.json"
```

Observacao: `JsonRepositoryDeps.py` define outro `DB_PATH` local. Isso reduz a utilidade deste arquivo como fonte unica de verdade.

## `logConfig.py`

Configura logging basico:

- arquivo: `infrastructure/logs/logs.log`;
- nivel: `INFO`;
- formato com data, nivel e mensagem.

## Comunicacao

`core` e usado por [[modulos/application]] e [[modulos/infrastructure]]. Ele deve permanecer sem dependencia das camadas externas.

