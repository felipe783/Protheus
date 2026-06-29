# Comunicacao Entre Camadas

Esta nota descreve como os modulos se comunicam no codigo atual.

## Fluxo HTTP atual

`api/main.py`

- cria `FastAPI()`;
- inclui `documentController`.

`api/routers/ControllerDocument.py`

- recebe `UploadFile`;
- le o conteudo em bytes;
- decodifica como UTF-8;
- chama `DocumentExtensionDetector.detect`;
- chama `DocumentTypeDetector.detect`;
- cria `DocumentInput`;
- chama `DocumentExtractor.extract`;
- retorna o dicionario extraido.

Ver [[fluxo/fluxo-http-atual]].

## Fluxo pretendido por caso de uso

`application/ExtractDocumentUseCase.py` sugere um fluxo mais limpo:

```text
file_content + filename
  -> DocumentExtensionDetector
  -> FileReaderFactory
  -> leitor concreto
  -> DocumentTypeDetector
  -> DocumentExtractor
  -> resposta com document_type e data
```

Ver [[fluxo/fluxo-caso-de-uso-pretendido]].

## Comunicacao com infraestrutura

`FileReaderFactory` instancia:

- `PdfReader`;
- `XmlReader`;
- `DocxReader`;
- `OdtReader`.

Esses leitores pertencem a [[modulos/infrastructure]].

## Comunicacao com core

`DocumentTypeDetector` depende de `core/DocumentKeyWords.py`.

`DocumentExtractor` depende de `core/DocumentPatternsRegex.py`.

`JsonRepositoryDeps` usa caminho local hardcoded para `infrastructure/db/db.json`, enquanto `core/dbPathConfig.py` tambem define `DB_PATH`. Essa duplicidade e um ponto de atencao.

