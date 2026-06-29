# Fluxo do Caso de Uso Pretendido

`application/ExtractDocumentUseCase.py` descreve um fluxo mais completo e alinhado com a arquitetura.

```text
file_content + filename
  -> DocumentExtensionDetector.detect(filename)
  -> FileReaderFactory.create(extension)
  -> reader.read(file_content)
  -> DocumentTypeDetector.detect(content, extension)
  -> DocumentExtractor.extract(content, document_type)
  -> { document_type, data }
```

## Intencao arquitetural

Esse fluxo centraliza a orquestracao em [[modulos/application]] e deixa [[modulos/api]] apenas como adaptador HTTP.

## Pontos positivos

- Usa extensao para escolher leitor.
- Evita regra de negocio dentro da rota.
- Facilita teste unitario do caso de uso.
- Aproxima o codigo da Clean Architecture descrita em [[arquitetura/arquitetura]].

## Ponto quebrado atualmente

Os leitores implementam `extract(path: str)`, mas o caso de uso chama `reader.read(file_content)`.

Para esse fluxo funcionar, uma destas decisoes deve ser tomada:

- alterar leitores para aceitarem bytes e metodo `read`;
- alterar o caso de uso para salvar temporariamente o arquivo e chamar `extract(path)`;
- padronizar a interface `FileReader`.

Ver [[arquitetura/observacoes-tecnicas]].

