# Documentação de Arquitetura — Projeto Protheus

> **Padrão arquitetural:** Clean Architecture + Domain-Driven Design (DDD)
> **Stack:** Python · FastAPI · JSON como persistência
> **Finalidade:** API para classificação e gerenciamento de documentos fiscais (NF-e, DANFE, XML)

---

## Visão Geral da Estrutura

```
Protheus/
├── main.py
├── api/
│   └── routers/
│       ├── deps.py
│       └── documents.py
├── application/
│   └── service/
│       ├── JSON.py
│       └── JSONservice.py
├── core/
│   ├── db_path_config.py
│   ├── document_classification.py
│   └── log_config.py
├── domain/
│   ├── interfaces/
│   │   └── documentRepositoryInterface.py
│   └── models/
│       ├── documentModel.py
│       ├── dcoument_type.py
│       ├── extensions_type.py
│       └── JSONRepository.py
├── infrastructure/
│   ├── db/
│   │   └── db.json
│   ├── http/
│   │   ├── request/        ← diretório reservado (vazio)
│   │   └── response/       ← diretório reservado (vazio)
│   └── persistence/
│       └── repository/
│           ├── entity/     ← diretório reservado (vazio)
│           └── jsonPersistence.py
├── test/
│   ├── test_db.py
│   └── test_log.py
└── docs/
    ├── arquitetura.md
    ├── arquitetura-clean-ddd-fastapi.md
    └── estrutura-clean-architecture(1).md
```

---

## Mapa das Camadas Arquiteturais

O projeto segue o modelo de **Clean Architecture** com 4 camadas concêntricas:

```
┌──────────────────────────────────────────────────┐
│                  API (Entrega)                   │  ← api/
│  ┌────────────────────────────────────────────┐  │
│  │           Application (Casos de Uso)       │  │  ← application/
│  │  ┌──────────────────────────────────────┐  │  │
│  │  │        Domain (Núcleo do negócio)    │  │  │  ← domain/
│  │  │  ┌────────────────────────────────┐  │  │  │
│  │  │  │   Infrastructure (Detalhes)    │  │  │  │  ← infrastructure/
│  │  │  └────────────────────────────────┘  │  │  │
│  │  └──────────────────────────────────────┘  │  │
│  └────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────┘
         core/ → transversal a todas as camadas
```

**Regra de dependência:** as setas sempre apontam de fora para dentro. Nenhuma camada interna conhece as externas.

---

## 1. `main.py` — Ponto de Entrada da Aplicação

**Responsabilidade:** Inicializar e configurar o servidor FastAPI, registrar os routers da API e subir a aplicação.

**Problema que resolve:** Centraliza o bootstrap da aplicação em um único arquivo, evitando que a inicialização fique espalhada pelo código.

**Regra técnica:** É o único arquivo que instancia o objeto `FastAPI()` e registra as rotas via `app.include_router()`. Não contém regras de negócio — apenas orquestra a montagem da aplicação. Referencia documentação externa de exemplo de XML de NF-e (`webdanfe.com.br`), indicando que o domínio envolve documentos fiscais.

---

## 2. Camada `api/` — Interface de Entrega HTTP

**Responsabilidade geral:** Receber requisições HTTP, validar entrada, chamar os serviços da camada Application e retornar respostas formatadas.

**Problema que resolve:** Isola o protocolo de comunicação (HTTP/REST) do restante do sistema. Se o sistema precisar trocar de protocolo (ex.: gRPC), apenas esta camada muda.

### `api/routers/deps.py` — Dependências Injetadas

**Responsabilidade:** Definir as dependências compartilhadas entre os endpoints usando o sistema de injeção de dependências do FastAPI (`Depends`).

**Problema que resolve:** Evita repetição de código nos endpoints. Em vez de instanciar repositórios ou serviços em cada rota, eles são declarados aqui e injetados automaticamente pelo framework.

**Regra técnica:** Funciona como uma fábrica de dependências. Centraliza a criação de instâncias de repositórios, serviços de autenticação, conexões com banco, etc. Qualquer endpoint que precise de uma instância de serviço declara o `Depends(get_service)` como parâmetro.

### `api/routers/documents.py` — Rotas de Documentos

**Responsabilidade:** Definir os endpoints HTTP relacionados a documentos (criação, consulta, listagem, exclusão). É o controller do módulo de documentos.

**Problema que resolve:** Agrupa todas as rotas de um mesmo recurso em um único arquivo (router), mantendo a organização por domínio funcional.

**Regra técnica:** Não contém lógica de negócio. Recebe a requisição, valida o schema com Pydantic e delega ao `ApplicationService`. Retorna a resposta ao cliente. Registrado no `main.py` via `app.include_router()`.

---

## 3. Camada `application/` — Casos de Uso

**Responsabilidade geral:** Orquestrar os fluxos de negócio (casos de uso). Coordena a interação entre o domínio e a infraestrutura sem conhecer detalhes de banco de dados ou HTTP.

**Problema que resolve:** Separa "o que o sistema faz" (casos de uso) de "como ele faz" (infraestrutura) e "como ele é exposto" (API).

### `application/service/JSON.py` — Utilitário JSON

**Responsabilidade:** Fornece funções utilitárias para serialização, desserialização e manipulação de dados JSON dentro dos casos de uso.

**Problema que resolve:** Centraliza a lógica de transformação de dados entre os modelos de domínio e a representação JSON, evitando código duplicado nos serviços.

**Regra técnica:** Não acessa banco diretamente nem conhece HTTP. Trabalha exclusivamente com transformação de dados em memória.

### `application/service/JSONservice.py` — Serviço Principal de Documentos

**Responsabilidade:** Implementar os casos de uso da aplicação — criar, consultar, listar e remover documentos. É a camada de serviço que implementa as regras de orquestração.

**Problema que resolve:** Contém a lógica de "como executar uma ação" (ex.: validar se um documento já existe antes de cadastrar, classificar o tipo do documento). Não sabe de onde vêm os dados (HTTP) nem onde serão salvos (JSON, banco de dados).

**Regra técnica:** Depende apenas de interfaces do domínio (`documentRepositoryInterface`), nunca de implementações concretas de infraestrutura. Isso permite trocar o banco de dados sem alterar nenhuma linha desta camada.

---

## 4. Camada `core/` — Configurações Transversais

**Responsabilidade geral:** Abrigar configurações e utilitários que são usados por todas as camadas do sistema. Funciona como infraestrutura interna, mas sem dependência de tecnologia externa.

**Problema que resolve:** Evita que configurações (caminhos de banco, regras de classificação, logs) fiquem acopladas a camadas específicas. Qualquer camada pode importar do `core/` sem criar dependências indevidas.

**Regra técnica:** Não deve importar nada das camadas `api/`, `application/`, `domain/` ou `infrastructure/`. Fluxo unidirecional: todos dependem do `core/`, nunca o contrário.

### `core/db_path_config.py` — Configuração do Caminho do Banco

**Responsabilidade:** Centralizar a configuração do caminho físico para o arquivo `db.json` (banco de dados JSON local).

**Problema que resolve:** Evita que strings de caminho de arquivo fiquem espalhadas pelo código. Se o arquivo de banco mudar de localização, apenas este arquivo precisa ser alterado.

**Regra técnica:** Deve ser a única fonte de verdade para o caminho do banco. Nenhum outro módulo deve hardcodar o caminho de `db.json`.

### `core/document_classification.py` — Classificação de Documentos

**Responsabilidade:** Implementar a lógica de classificação de documentos fiscais por tipo e extensão. Determina se um arquivo é NF-e, XML, PDF, DANFE, etc.

**Problema que resolve:** Concentra as regras de negócio de classificação em um único lugar. Evita que a lógica de "qual tipo é esse documento?" fique duplicada em serviços e controllers.

**Regra técnica:** Trabalha com os enumeradores definidos em `domain/models/dcoument_type.py` e `domain/models/extensions_type.py`. É uma regra de negócio pura — sem acesso a banco ou rede.

### `core/log_config.py` — Configuração de Logging

**Responsabilidade:** Configurar o sistema de logs da aplicação (nível de log, formato de saída, handlers). Define como e onde os logs serão registrados.

**Problema que resolve:** Centraliza a configuração de logging para toda a aplicação. Sem isso, cada módulo criaria seu próprio logger com configurações inconsistentes.

**Regra técnica:** Deve ser importado no início da execução (em `main.py`). Todos os demais módulos importam apenas `logging.getLogger(__name__)` — nunca reconfiguram o logger.

---

## 5. Camada `domain/` — Núcleo do Negócio

**Responsabilidade geral:** Representar as entidades, regras de negócio e contratos (interfaces) do domínio. É a camada mais interna e estável do sistema — não depende de nenhuma outra camada.

**Problema que resolve:** Garante que as regras de negócio não fiquem contaminadas por detalhes técnicos de banco de dados, HTTP ou bibliotecas externas.

**Regra técnica (DDD):** Nenhuma classe deste pacote deve importar de `api/`, `application/` ou `infrastructure/`. Dependências do domínio são apenas de si próprio e do Python padrão.

### `domain/interfaces/documentRepositoryInterface.py` — Contrato do Repositório

**Responsabilidade:** Definir a interface (contrato) que qualquer implementação de repositório de documentos deve seguir. Declara os métodos que precisam existir (`save`, `find_by_id`, `list_all`, `delete`), sem implementá-los.

**Problema que resolve:** Desacopla o domínio da infraestrutura. A camada `application` depende dessa interface, não da implementação concreta em JSON ou banco de dados. Isso segue o **Princípio da Inversão de Dependência (DIP)**.

**Regra técnica:** Em Python, implementada como `ABC` (Abstract Base Class) ou `Protocol`. A infraestrutura implementa esta interface; o domínio nunca importa de `infrastructure/`.

### `domain/models/documentModel.py` — Entidade Documento

**Responsabilidade:** Definir a entidade central do domínio — o Documento. Representa os atributos e invariantes de um documento fiscal (ID, nome, tipo, extensão, conteúdo, data de criação).

**Problema que resolve:** Cria um modelo rico que encapsula as regras de um documento válido. Centraliza o que é um documento no contexto do sistema.

**Regra técnica:** É um modelo Pydantic (ou dataclass). Deve validar seus próprios campos na instanciação. Não contém lógica de persistência.

### `domain/models/dcoument_type.py` — Enumerador de Tipos de Documento

**Responsabilidade:** Definir os tipos de documento suportados pelo sistema (ex.: `NF_E`, `DANFE`, `XML`, `PDF`, `OUTRO`).

**Problema que resolve:** Substitui strings mágicas (`"xml"`, `"pdf"`) por um enumerador tipado, evitando erros de digitação e facilitando a manutenção.

**Regra técnica:** Implementado como `Enum` do Python. Deve ser usado em todos os módulos que precisam referenciar tipos de documento — nunca usar strings literais.

> **Nota:** O nome do arquivo contém um erro de digitação (`dcoument` em vez de `document`). Recomenda-se renomear para `document_type.py` para manter consistência com os demais arquivos.

### `domain/models/extensions_type.py` — Enumerador de Extensões

**Responsabilidade:** Definir as extensões de arquivo suportadas pelo sistema (ex.: `.xml`, `.pdf`, `.json`).

**Problema que resolve:** Centraliza as extensões válidas como enumerador, permitindo que `core/document_classification.py` valide extensões de forma segura e tipada.

**Regra técnica:** Complementa `dcoument_type.py`. A relação entre extensão e tipo de documento é resolvida por `document_classification.py` no `core/`.

### `domain/models/JSONRepository.py` — Modelo de Repositório JSON

**Responsabilidade:** Definir a estrutura de dados do banco JSON — como os documentos são organizados dentro do arquivo `db.json`.

**Problema que resolve:** Separa o "contrato de dados" da implementação de leitura/escrita. Define o schema esperado no arquivo JSON.

**Regra técnica:** Este modelo descreve a estrutura em nível de domínio. Não acessa o arquivo diretamente — isso é responsabilidade de `jsonPersistence.py` na infraestrutura.

---

## 6. Camada `infrastructure/` — Detalhes Técnicos e Externos

**Responsabilidade geral:** Implementar os detalhes técnicos do sistema: persistência de dados, comunicação HTTP, acesso a arquivos. É a camada mais externa e mais volátil — a que mais muda com o tempo.

**Problema que resolve:** Isola tecnologias concretas (arquivo JSON, HTTP client) para que o restante do sistema não precise conhecê-las.

**Regra técnica:** Implementa as interfaces definidas no domínio. Depende do domínio, nunca o contrário.

### `infrastructure/db/db.json` — Banco de Dados JSON

**Responsabilidade:** Armazenar os documentos cadastrados no sistema em formato JSON local. É o banco de dados concreto da aplicação.

**Problema que resolve:** Fornece persistência simples sem necessidade de instalação de SGBD. Adequado para prototipação e sistemas de baixo volume.

**Regra técnica:** Inicializado com estrutura vazia `{ "documents": [] }`. Nunca deve ser acessado diretamente pelos serviços — apenas via `jsonPersistence.py`. Em produção, este arquivo deve ser substituído por um banco relacional ou NoSQL sem que o domínio mude.

### `infrastructure/persistence/repository/jsonPersistence.py` — Implementação do Repositório

**Responsabilidade:** Implementar concretamente a interface `documentRepositoryInterface` usando o arquivo `db.json` como meio de persistência. Realiza leitura, escrita, atualização e remoção de documentos no arquivo JSON.

**Problema que resolve:** Traduz operações abstratas do domínio (`save(document)`) em operações concretas de arquivo (`json.load()`, `json.dump()`).

**Regra técnica:** Esta classe implementa todos os métodos definidos em `documentRepositoryInterface.py`. É registrada como implementação no mecanismo de injeção de dependências (via `deps.py`). Nenhuma camada além de `application/` deve instanciá-la diretamente.

### `infrastructure/persistence/repository/entity/` — Diretório Reservado para Entidades

**Responsabilidade:** Reservado para futuras classes de mapeamento entre entidades do domínio e a representação no banco de dados (padrão Entity/DAO).

**Problema que resolve:** Quando o sistema migrar para um banco relacional, este diretório conterá os modelos ORM (SQLAlchemy, por exemplo), separando o modelo de domínio do modelo de banco.

**Regra técnica:** Atualmente vazio. Não deve ser usado para lógica de negócio — apenas para mapeamentos técnicos de persistência.

### `infrastructure/http/request/` — Diretório Reservado para Clientes HTTP de Entrada

**Responsabilidade:** Reservado para schemas e modelos de requisições HTTP de entrada — DTOs (Data Transfer Objects) que representam o corpo de requisições recebidas.

**Problema que resolve:** Ao crescer, o sistema poderá ter schemas de validação de entrada separados dos modelos de domínio, permitindo evoluir a API sem afetar o domínio.

### `infrastructure/http/response/` — Diretório Reservado para Modelos de Resposta

**Responsabilidade:** Reservado para schemas e modelos de respostas HTTP — DTOs de saída que definem o formato JSON retornado aos clientes da API.

**Problema que resolve:** Permite controlar o que é exposto na API independentemente do modelo interno do domínio, seguindo o padrão de API Contract.

---

## 7. Camada `test/` — Testes Automatizados

**Responsabilidade geral:** Validar o comportamento correto dos componentes do sistema. Garante que mudanças futuras não introduzam regressões.

**Regra técnica:** Testes não devem importar de `api/` ou `infrastructure/` quando estão testando o domínio. Cada teste deve ser independente e não alterar o `db.json` real.

### `test/test_db.py` — Testes de Persistência

**Responsabilidade:** Testar a camada de persistência JSON — verificar que documentos são corretamente salvos, lidos e removidos do `db.json`.

**Problema que resolve:** Garante que `jsonPersistence.py` funciona corretamente e que o banco JSON mantém integridade após operações de escrita e leitura.

**Regra técnica:** Deve usar um arquivo JSON de teste isolado (não o `db.json` de produção). O arquivo de teste deve ser limpo antes e após cada execução de teste.

### `test/test_log.py` — Testes de Logging

**Responsabilidade:** Verificar que o sistema de logging está configurado corretamente e que os eventos esperados são registrados nos níveis adequados.

**Problema que resolve:** Garante que `core/log_config.py` produz logs no formato e nível corretos, evitando que erros críticos passem sem registro.

---

## 8. `docs/` — Documentação Técnica

**Responsabilidade:** Centralizar a documentação arquitetural do projeto para consulta da equipe.

### `docs/arquitetura.md`

**Responsabilidade:** Documento geral de arquitetura do sistema — visão macro das camadas, decisões técnicas e justificativas de design.

### `docs/arquitetura-clean-ddd-fastapi.md`

**Responsabilidade:** Documentação específica sobre a aplicação dos padrões Clean Architecture e DDD com FastAPI neste projeto. Explica como os conceitos foram adaptados para a stack escolhida.

### `docs/estrutura-clean-architecture(1).md`

**Responsabilidade:** Descrição detalhada da estrutura de diretórios, explicando o papel de cada pasta. Provavelmente o documento de referência para novos desenvolvedores entrarem no projeto.

---

## Fluxo de uma Requisição (Fim a Fim)

```
Cliente HTTP
    │
    ▼
api/routers/documents.py       ← recebe a requisição, valida schema
    │
    ▼
application/service/JSONservice.py  ← executa o caso de uso
    │  (usa interface do domínio)
    ▼
domain/interfaces/documentRepositoryInterface.py  ← contrato abstrato
    │  (implementado por)
    ▼
infrastructure/persistence/repository/jsonPersistence.py  ← acessa o arquivo
    │
    ▼
infrastructure/db/db.json      ← dados persistidos
```

**Transversais em todas as etapas:**
- `core/log_config.py` → logging em todas as camadas
- `core/document_classification.py` → chamado pelo serviço para classificar documentos
- `core/db_path_config.py` → usado por `jsonPersistence.py` para localizar o arquivo

---

## Problemas Identificados e Recomendações

| Problema | Localização | Recomendação |
|---|---|---|
| Erro de digitação no nome do arquivo | `domain/models/dcoument_type.py` | Renomear para `document_type.py` |
| `JSONRepository.py` no domínio | `domain/models/JSONRepository.py` | Mover para `infrastructure/persistence/repository/` — detalhes de JSON não pertencem ao domínio |
| `JSON.py` no application | `application/service/JSON.py` | Renomear para algo mais descritivo como `serialization.py` |
| Diretórios `entity/`, `request/`, `response/` vazios | `infrastructure/` | Documentar intenção ou criar arquivos `__init__.py` com docstring explicando o propósito |
| Banco em JSON | `infrastructure/db/db.json` | Adequado para MVP; planejar migração para PostgreSQL ou SQLite conforme o volume crescer |

---

## Resumo por Camada

| Camada         | Pasta              | Conhece          | É conhecida por                     |
|----------------|--------------------|------------------|-------------------------------------|
| Domínio        | `domain/`          | Ninguém          | Application, Infrastructure         |
| Aplicação      | `application/`     | Domain           | API                                 |
| Infraestrutura | `infrastructure/`  | Domain           | Application (via interface)         |
| API/Entrega    | `api/`             | Application      | Ninguém (ponto de entrada)          |
| Transversal    | `core/`            | Ninguém          | Todos                               |
| Testes         | `test/`            | Todos            | Ninguém                             |
| Documentação   | `docs/`            | —                | —                                   |
