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

- [[Extrator e Detector]]: `DocumentTypeDetector` e `DocumentExtractor` (usados pelo `ExtractDocumentUseCase`).
- `DocumentExtensionDetector`: converte `Path(filename).suffix` em `documentExtension`; lança `ValueError` para extensões não suportadas.
- [[Inputs e Outputs (Protheus)|Inputs e Outputs]]: `DocumentInput` é usado pelo caso de uso; `DocumentOutput` existe mas o endpoint retorna o `dict` cru.
- `ExtractDocumentUseCase.py`: **orquestra o fluxo de extração** desde 2026-10-18 (antes estava no [[Controller (Protheus)|Controller]]).

## ExtractDocumentUseCase

- Recebe no construtor um `DocumentRepository` (a interface de `domain/interfaces`). A implementação concreta, o [[JSON Repository]], é escolhida pela API. Assim a `application` não importa diretamente a persistência da `infrastructure` (a ressalva é a Factory, que ainda importa os readers).
- `execute(file_content: bytes, filename: str) -> dict`:
  1. `DocumentExtensionDetector.detect(filename)`;
  2. grava os bytes num temporário com `suffix=extension.value` (ex.: `.pdf`), porque os readers recebem um **caminho**;
  3. `FileReaderFactory.get(extension).extract(tmp_path)` e apaga o temporário no `finally`;
  4. `DocumentTypeDetector.detect` → `DocumentInput` → `DocumentExtractor.extract`;
  5. monta o `Document`, registra com `logging.debug` e chama `repository.save(document)`;
  6. retorna o `dict` extraído.
- Testado em `test/test_use_case.py` com `test.xml` e banco temporário (`monkeypatch` em `core.dbPathConfig.DB_PATH`).