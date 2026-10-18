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

### Método `getAll`

Lê todos os registros do JSON e os converte de volta para `Document` via `DocumentEntity.toDomain()`.

````python
    def getAll(self) -> list[Document]:
        data = get_db()
        return [
            DocumentEntity(**item).toDomain()
            for item in data["documents"]
        ]
````

> [!note] Estado atual (2026-10-18)
> A classe **é usada no fluxo**: o [[Controller (Protheus)|Controller]] a injeta no `ExtractDocumentUseCase`, que chama `save`. Os imports foram corrigidos para importar as **classes** (`from domain.interfaces.DocumentRepository import DocumentRepository`, `from infrastructure.persistence.entity.DocumentEntity import DocumentEntity`). Antes, herdar de um módulo quebrava o carregamento com `TypeError: module() takes at most 2 arguments`, confirmado em execução.
> O `__dict__` da entidade grava `type`/`extension` como texto (`"crlv_e"`, `".odt"`), porque os enums herdam de `str`. O formato é o mesmo que o controller gravava antes.

> [!warning] `getAll` não reconverte os tipos
> `getAll` não é chamado por nenhuma rota. Ele monta `DocumentEntity(**item)` direto do JSON, então `created_in`, `type` e `extension` voltam como `str`, não como `datetime` e enums. Não verificado em execução.
