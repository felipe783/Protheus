# Estrutura do Projeto

```text
Protheus/
	📁 FrontEnd
	|  |--index.html
	|  |--script.js
	|  |--style.css
	📁 api
	|  |--📁 routers
	|  |  |--ControllerDocument.py
	|  |--__init__.py
	|  |--main.py
	📁 application
	|  |--📁 input
	|  |  |--DocumentInput.py
	|  |--📁 output
	|  |  |--DocumentOutput.py
	|  |--DocumentExtensionDetector.py
	|  |--DocumentExtractor.py
	|  |--DocumentTypeDetector.py
	|  |--ExtractDocumentUseCase.py
	📁 core
	|  |--📁 Logs
	|  |  |--LogUploadConfig.py
	|  |--DocumentKeyWords.py
	|  |--DocumentPatternsRegex.py
	|  |--dbPathConfig.py
	📁 domain
	|  |--📁 interfaces
	|  |  |--DocumentExtractor.py
	|  |  |--DocumentRepository.py
	|  |  |--FileReader.py
	|  |--📁 models
	|     |--Document.py
	|     |--DocumentExtension.py
	|     |--DocumentType.py
	|     |--DocumentUUID.py
	|     |--FileReaderFactory.py
	📁 infrastructure
	|  |--📁 db
	|  |  |--db.json
	|  |--📁 logs
	|  |  |--uploads_logs.log
	|  |--📁 persistence
	|  |  |--📁 entity
	|  |  |  |--DocumentEntity.py
	|  |  |--📁 repository
	|  |     |--JsonDocumentRepository.py
	|  |     |--JsonRepositoryDeps.py
	|  |--📁 readers
	|     |--DocxReader.py
	|     |--OdtReader.py
	|     |--PdfReader.py
	|     |--XmlReader.py
```
## Pastas

- `api/`: entrada HTTP. Ver [[Main]].
- `routers/`: rotas da API, Ver [[!Modulo API]]
- `application/`: casos de uso, detectores e extrator. Ver [[!Modulo Application]].
- `core/`: configuracoes e constantes transversais. Ver [[!Modulo Core]].
- `domain/`: modelos e interfaces. Ver [[!Modulo Domain]].
- `infrastructure/`: implementacoes tecnicas. Ver [[!Modulo Insfraestrutura]].

