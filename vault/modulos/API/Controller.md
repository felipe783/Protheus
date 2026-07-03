# Sobre o Arquivo

O Arquivo `controller` é o **Orquestrador das Requisições** é nele onde são feitas as principais chamadas entre os arquivos.

Responsabilidades:
- criar o `Endpoint`
- Receber os Arquivo que foi dado Upload pelo Usuário
- Retornar a resposta HTTP
# Funcionalidades

## Criação EndPoint:

````python
	documentController = APIRouter(
		prefix="/document",
		tags=["document"]
	)
````
## Upload dos Arquivos

- A API recebe o arquivo via FastAPI, realiza a leitura do conteúdo, identifica sua extensão e, em seguida, cria um arquivo temporário para processamento posterior.

````python
	async def extract_document(file: UploadFile = File(...)):
	    content = await file.read()
	    extension = DocumentExtensionDetector.detect(file.filename)
	  
		with tempfile.NamedTemporaryFile(
			delete=False,
			suffix=f".{extension.value}"
		)as tmp:
		        tmp.write(content)
		        tmp_path = tmp.name	
````
# Filtragem por Factory

- Com o arquivo temporário criado, o "controller" aciona a [[Factory]], que seleciona o [[Reader PDF]] adequado para cada extensão. Em seguida, o "reader" processa o arquivo e realiza a extração do conteúdo, convertendo-o para texto puro.

````python
	try:
		reader = FileReaderFactory.get(extension)
		text = reader.extract(tmp_path)
	finally: # Fecha o Arquivo Temp
	    os.unlink(tmp_path)
````

# Extração das Informações

- Com a ``Factory`` e o ``Reader`` selecionados, o arquivo passa por uma etapa de análise para identificar seu tipo por meio da função `detect` do [[Extrator e Detector|"DocumentTypeDetector.py"]].Com o tipo já definido, os dados são encapsulados em um [[Inputs e Outputs#Document input input-doc |DTO de Input]]. Em seguida, esse contexto é utilizado pelo [[Extrator e Detector#DocumentExtractor extractor|DocumentExtractor]] para realizar a extração e processamento do conteúdo do documento.

````python
	documentType = DocumentTypeDetector.detect(
		content=text,
		extension=extension
	)
	documentInput = DocumentInput(
		created_in=datetime.now(),
		type=documentType,
		extension=extension
	)
	result = DocumentExtractor.extract(
		content=text,
		document_type=documentInput.type
	)
````

# Salvar no JSON

- O código cria uma entidade [[Models#Document document|Document]] a partir dos dados processados do documento. Em seguida, registra essa entidade no log, depois converte o objeto de dominio para uma Entidade de Persistencia[[JSON Repository#DocumentEntity document-entity|(DocumentEntity)]], carrega um banco JSON em memória e adiciona o novo documento na lista,por fim no JSON

````python
	document = Document(
		id=DocumentUUID.generate(),
		created_in=documentInput.created_in,
		description=result,
		type=documentInput.type,
		extension=documentInput.extension
	)
    logging.debug(document)
    entity = DocumentEntity.fromDomain(document) # Converter do dominio -> Json
    db = get_db()

    db["documents"].append({
        "id": entity.id,
        "created_in": entity.created_in,
        "description": entity.description,
        "type": entity.type.value,
        "extension": entity.extension.value
    })
    save_db(db)    
````