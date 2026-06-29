# Estrutura do Projeto

Estrutura relevante detectada:

```text
Protheus/
  api/
    __init__.py
    main.py
    routers/ControllerDocument.py
  application/
    DocumentExtensionDetector.py
    DocumentExtractor.py
    DocumentTypeDetector.py
    ExtractDocumentUseCase.py
    input/DocumentInput.py
    output/DocumentOutput.py
  core/
    dbPathConfig.py
    logConfig.py
    DocumentKeyWords.py
    DocumentPatternsRegex.py
  domain/
    interfaces/
      FileReader.py
      DocumentRepository.py
      DocumentExtractor.py
    models/
      Document.py
      DocumentUUID.py
      DocumentType.py
      DocumentExtension.py
      FileReaderFactory.py
  infrastructure/
    db/db.json
    logs/logs.log
    readers/
      PdfReader.py
      XmlReader.py
      DocxReader.py
      OdtReader.py
    persistence/
      entity/DocumentEntity.py
      repository/JsonDocumentRepository.py
      repository/JsonRepositoryDeps.py
  test/
    test_db.py
    test_log.py
  docs/
    arquitetura.md
    arquitetura-clean-ddd-fastapi.md
    documentacao-estrutura-protheus.md
    estrutura-clean-architecture(1).md
  test.xml
  documento_empresa.pdf
  documento_empresa.odt
  .gitignore
```

## Pastas

- `api/`: entrada HTTP. Ver [[modulos/api]].
- `application/`: casos de uso, detectores e extrator. Ver [[modulos/application]].
- `core/`: configuracoes e constantes transversais. Ver [[modulos/core]].
- `domain/`: modelos e interfaces. Ver [[modulos/domain]].
- `infrastructure/`: implementacoes tecnicas. Ver [[modulos/infrastructure]].
- `test/`: testes com pytest. Ver [[modulos/testes]].
- `docs/`: documentacao existente, parcialmente desatualizada em relacao ao codigo atual.
- `vault/`: documentacao Obsidian gerada.

## Arquivos da raiz

- `.gitignore`: regras de exclusao do Git.
- `test.xml`: amostra de XML.
- `documento_empresa.pdf`: amostra PDF.
- `documento_empresa.odt`: amostra ODT.

