# Json Repository

O Arquivo `JsonDocumentRepository` é uma implementação concreta da interface `DocumentRepository`, responsável por persistir e recuperar documentos utilizando um armazenamento baseado em JSON, ele atua como uma camada de infraestrutura, isolando o domínio dos detalhes de persistência em arquivo.
## Responsabilidade

Essa classe tem duas responsabilidades principais:
- salvar documentos no arquivo JSON;
- recuperar todos os documentos armazenados e convertê-los para o modelo de domínio.
### Método `save`

O método `save(self, document)` persiste um documento no “banco” JSON.

````python
	def save(self, document):
        data = get_db()
        data["documents"].append(DocumentEntity.fromDomain(document).__dict__)
        save_db(data)
	    return document
````