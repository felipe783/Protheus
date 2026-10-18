O módulo **`application`** é responsável por **orquestrar os casos de uso da aplicação**. É nessa camada que ficam os fluxos que coordenam as regras de negócio, chamando os componentes do domínio e da infraestrutura para executar uma funcionalidade completa.

Normalmente, esse módulo contém:
- **Use Cases**
    - Implementam as funcionalidades do sistema, coordenando todas as etapas necessárias para atender uma requisição.
- **Services (quando utilizados)**
    - Agrupam operações da aplicação que podem ser reutilizadas por diferentes casos de uso.
- **Interfaces (Ports)**
    - Definem contratos que serão implementados pela camada de infraestrutura, promovendo baixo acoplamento.
- **Orquestração do fluxo**
    - Coordena chamadas para repositórios, serviços externos e componentes do domínio, sem conhecer detalhes de implementação.

## No Protheus

- [[Extrator e Detector]]: `DocumentTypeDetector` e `DocumentExtractor` (usados pelo [[Controller (Protheus)|Controller]]).
- `DocumentExtensionDetector`: converte `Path(filename).suffix` em `documentExtension`; lança `ValueError` para extensões não suportadas.
- [[Inputs e Outputs (Protheus)|Inputs e Outputs]]: `DocumentInput` é usado; `DocumentOutput` existe mas o controller retorna o `dict` cru.
- `ExtractDocumentUseCase.py`: **não é usado e não funciona** no estado atual — chama `FileReaderFactory.create(...)` e `reader.read(file_content)`, mas a factory só tem `get` e os readers implementam `extract(path)`. É o ponto natural para tirar a orquestração do controller.