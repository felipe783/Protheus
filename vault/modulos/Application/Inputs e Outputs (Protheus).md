> Todas essas classes são DTO(Data Transfer Object)
# Sobre os Arquivos

Estes arquivos é o **Responsável pela Transferência de Dados** entre as camadas da aplicação. Nele são definidos os objetos de `Input` e `Output`, que padronizam as informações recebidas e retornadas pelos casos de uso, reduzindo o acoplamento e facilitando a validação e a manutenção do sistema.
# Document Input

Responsabilidade:
- É o **Responsável por receber e organizar os dados de entrada** necessários para a execução de um caso de uso, garantindo que as informações sejam passadas de forma padronizada entre as camadas.

Código:

````python
@dataclass(frozen=True)
class DocumentInput:
	created_in: datetime
	type: documentType
	extension: documentExtension
````
# Document Output

Responsabilidade:
- É o **Responsável por transportar e padronizar os dados de saída** gerados por um caso de uso, definindo quais informações serão retornadas para a camada que realizou a solicitação.

Código:

````python
@dataclass(frozen=True)
class DocumentOutput:
    id: str
    created_in: datetime
    description: dict[str, str | None]
    type: documentType
    extension: documentExtension

    @classmethod
    def fromDocument(cls, document: Document): # Recebe um Document e transforma em output(é basicamente uma Factory)
        return cls(
            id=str(document.id.uuid),
            created_in=document.created_in,
            description=document.description,
            type=document.type,
            extension=document.extension
        )
````


