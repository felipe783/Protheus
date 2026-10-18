# Sobre o Arquivo

A classe `DocumentEntity` é um **Data Transfer / Persistence Model**, responsável por representar o documento na camada de infraestrutura (ou persistência), servindo como ponte entre o domínio e o armazenamento externo.
# Funcionalidades

## Método `toDomain`

O método `toDomain()` é responsável por converter a entidade de infraestrutura para o modelo de domínio.

````python
	def toDomain(self) -> Document
        return Document(
            id=DocumentUUID(self.id),
            created_in=self.created_in,
            description=self.description,
            type=self.type,
            extension=self.extension
        )
````

## Método `fromDomain`

O método `fromDomain()` realiza o processo inverso, convertendo o modelo de domínio para a entidade persistível, ele:
- transforma `DocumentUUID` em `str` (`document.id.uuid`);
- mantém os demais campos no formato necessário para persistência.

````python
	@classmethod
    def fromDomain(cls, document: Document):
        return cls(
            id=str(document.id.uuid),
            created_in=document.created_in,
            description=document.description,
            type= document.type,
            extension= document.extension
        )
````

---
**Projeto Pai:** [[_Protheus]] · **Módulo:** [[!Modulo Infraestrutura (Protheus)|!Modulo Infraestrutura]]
