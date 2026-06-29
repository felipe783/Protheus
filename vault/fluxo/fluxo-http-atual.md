# Fluxo HTTP Atual

Este e o fluxo realmente executado por `POST /document/extract`.

```text
Cliente
  -> POST /document/extract
  -> UploadFile
  -> file.read()
  -> bytes.decode("utf-8", errors="ignore")
  -> DocumentExtensionDetector.detect(filename)
  -> DocumentTypeDetector.detect(content, extension)
  -> DocumentInput(...)
  -> DocumentExtractor.extract(content, document_type)
  -> dict de campos extraidos
```

## Passo a passo

1. Cliente envia um arquivo.
2. `ControllerDocument.extract_document` le o conteudo completo.
3. O conteudo e decodificado como UTF-8.
4. A extensao e detectada pelo nome do arquivo.
5. O tipo do documento e detectado por XML tags ou keywords.
6. `DocumentInput` e criado com data, tipo e extensao.
7. `DocumentExtractor` consulta os regex em `DOCUMENT_PATTERNS`.
8. A API retorna os dados extraidos.

## Limitacao

Esse fluxo nao usa os leitores especificos de [[modulos/infrastructure]]. Por isso, PDFs, DOCX e ODT podem nao ser processados corretamente no endpoint atual.

## Modulos envolvidos

- [[modulos/api]]
- [[modulos/application]]
- [[modulos/core]]
- [[modulos/domain]]

