# Modulo Application

O modulo `application` concentra detectores, extrator e caso de uso.

## `DocumentExtensionDetector.py`

Detecta a extensao do arquivo usando `Path(filename).suffix.lower()`.

Retorna um valor de `documentExtension`:

- `.pdf`;
- `.xml`;
- `.docx`;
- `.odt`;
- vazio/desconhecido.

Se a extensao nao estiver no enum, levanta `ValueError`.

## `DocumentTypeDetector.py`

Classifica o tipo do documento.

Para XML:

- se encontrar `<nfe`, retorna `DANFE_XML`;
- se encontrar `<infnfe`, retorna `DANFE_XML`;
- caso contrario, retorna `DESCONHECIDO`.

Para outros formatos:

- baixa o conteudo para lowercase;
- calcula pontuacao por keywords em `core/DocumentKeyWords.py`;
- escolhe o tipo com maior score;
- se nenhum score for maior que zero, retorna `DESCONHECIDO`.

Conecta-se a [[modulos/core]] e [[modulos/domain]].

## `DocumentExtractor.py`

Extrai campos usando regex.

Fluxo:

```text
document_type
  -> DOCUMENT_PATTERNS.get(document_type)
  -> re.search para cada campo
  -> dict com valores ou None
```

Os padroes ficam em [[modulos/core]].

## `ExtractDocumentUseCase.py`

Caso de uso pretendido para extracao completa.

Entrada:

- `file_content: bytes`;
- `filename: str`.

Fluxo pretendido:

1. Detecta extensao.
2. Cria leitor via `FileReaderFactory`.
3. Le conteudo.
4. Detecta tipo documental.
5. Extrai dados.
6. Retorna `{ "document_type": ..., "data": ... }`.

Ver [[fluxo/fluxo-caso-de-uso-pretendido]].

## DTOs

### `application/input/DocumentInput.py`

Dataclass imutavel com:

- `created_in`;
- `type`;
- `extension`.

### `application/output/DocumentOutput.py`

Dataclass imutavel para resposta a partir de `Document`.

Campos:

- `id`;
- `created_in`;
- `description`;
- `type`;
- `extension`.

