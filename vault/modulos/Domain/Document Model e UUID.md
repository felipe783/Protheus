# Sobre os arquivos^document

O arquivo ``Document`` define a classe `Document`, que representa a **entidade de um documento** dentro do sistema, reunindo todas as informações relacionadas a um documento processado, e com isso o arquivo [[Document Model e UUID#Document UUID uuid|Document UUID]] define seu UUID
# Document^model-doc
## Funcionalidade

Primeiramente, a classe é definida utilizando a anotação `@dataclass`, que gera automaticamente alguns métodos especiais, como por exemplo:

- `__init__()` → inicializa os atributos da classe (construtor);
- `__repr__()` → retorna uma representação do objeto, útil para depuração;
- `__eq__()` → permite comparar dois objetos verificando se seus atributos possuem os mesmos valores.

Depois disso a classe implementa o método `__str__()`, responsável por definir uma representação do objeto quando ele é exibido com `print()` ou convertido para `str()`. Esse método é equivalente ao `toString()` da linguagem Java.

````python
@dataclass
class Document:
    id: DocumentUUID
    created_in: datetime
    description: dict[str, str | None]
    type: documentType
    extension: documentExtension

    def __str__(self):
        return (
            f"\nDocument(\n"
            f"  id={self.id},\n"
            f"  created_in={self.created_in},\n"
            f"  description={self.description},\n"
            f"  type={self.type},\n"
            f"  extension={self.extension}\n"
            f")"
        )
````

# Document UUID^uuid# Funcionalidade

Ela serve para garantir que o ID do documento:
- seja sempre um **UUID válido**;
- tenha uma **representação consistente dentro do sistema**;
- seja tratado como um **tipo próprio (`DocumentUUID`)**, evitando o uso de strings soltas.

Inicialmente, a classe utiliza o método `__init__` para realizar a inicialização e validação do valor recebido. Nesse processo:
- recebe uma string `uuid_str`;
- converte essa string para um objeto `uuid.UUID` nativo do Python;
- armazena o resultado em `self.uuid`.

Essa conversão garante que qualquer valor armazenado seja um UUID válido desde a criação do objeto, além disso, o método `generate` é responsável por criar um novo UUID válido automaticamente, utilizando a geração padrão do módulo `uuid` do Python.
````python
class DocumentUUID:
    def __init__(self, uuid_str: str):
        self.uuid = UUID(uuid_str)
    @classmethod
    def generate(cls):
        return cls(str(uuid4()))
````