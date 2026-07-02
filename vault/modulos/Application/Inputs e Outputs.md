> Todas essas classes sao DTO(Data Transfer Object)
# Document input^input-doc

- Esta classe reúne reune os dados necessários para a execução de um caso de uso. Dessa forma, evita-se passar vários parâmetros para um mesmo método

````python
@dataclass(frozen=True)
class DocumentInput:
	created_in: datetime
	type: documentType
	extension: documentExtension
```