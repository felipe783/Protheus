# Modulo Domain

O modulo `domain` representa o nucleo do sistema.

## Models

### `DocumentType.py`

Enum `documentType`:

- `CRLV_E`;
- `CARTAO_CNPJ`;
- `DANFE_XML`;
- `LAUDO`;
- `CONTRATO`;
- `DESCONHECIDO`.

Usado por [[modulos/application]] para classificacao e extracao.

### `DocumentExtension.py`

Enum `documentExtension`:

- `.pdf`;
- `.xml`;
- `.docx`;
- `.odt`;
- vazio/desconhecido.

Usado por `DocumentExtensionDetector` e `FileReaderFactory`.

### `Document.py`

Dataclass que representa um documento:

- `id`;
- `created_in`;
- `description`;
- `type`;
- `extension`.

Observacao: os imports atuais usam `models.*`, mas o pacote real esta em `domain.models.*`. Ver [[arquitetura/observacoes-tecnicas]].

### `DocumentUUID.py`

Wrapper simples para validar/conter `UUID`.

### `FileReaderFactory.py`

Fabrica leitores por extensao:

- `.pdf` -> `PdfReader`;
- `.xml` -> `XmlReader`;
- `.docx` -> `DocxReader`;
- `.odt` -> `OdtReader`.

Embora esteja em `domain/models`, ela importa classes concretas de [[modulos/infrastructure]], o que cria dependencia do dominio para infraestrutura.

## Interfaces

### `FileReader.py`

Contrato abstrato:

```python
extract(self, path: str) -> str
```

### `DocumentRepository.py`

Contrato abstrato:

```python
save(self, document)
```

### `DocumentExtractor.py`

Contrato abstrato:

```python
extract(self, content: str) -> dict
```

## Papel no sistema

O dominio define o vocabulário tecnico do projeto. Termos como `Document`, `documentType` e `documentExtension` sao explicados em [[glossary/glossary]].

