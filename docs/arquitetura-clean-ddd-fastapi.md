# Clean Architecture + DDD + FastAPI — Guia da Estrutura do Projeto

Este documento explica a estrutura de pastas usada no projeto, os princípios por trás dela (Clean Architecture + DDD), e traz uma estrutura alternativa comum em projetos FastAPI para comparação.

---

## 📁 Visão geral da estrutura atual

```
app/
 ├── api/
 ├── application/
 ├── core/
 ├── domain/
 ├── infrastructure/
 ├── main.py
 └── test/
```

A ideia central é separar o sistema em **camadas com responsabilidades isoladas**, seguindo a regra de dependência da Clean Architecture: as camadas internas (domínio) não conhecem as externas (infraestrutura, API).

**Fluxo de dependência:**

```
Request (API)
   ↓
Caso de uso (application)
   ↓
Regras puras (domain)
   ↓
Banco / JSON / API externa (infrastructure)
```

---

## 🌐 1. `api/` — Camada de entrada

Responsável por:

- Rotas do FastAPI
- Schemas de request/response (validação de entrada e saída via HTTP)
- Injeção de dependências (`Depends`)

Exemplo:

```python
@router.post("/upload")
def upload(file: UploadFile):
    ...
```

> 📌 **Aqui NÃO fica regra de negócio.** A rota apenas recebe a requisição e delega para a camada de aplicação.

---

## 🧠 2. `application/` — Casos de uso

É o "cérebro operacional" do sistema: orquestra as regras de negócio sem implementá-las diretamente (isso é papel do `domain`).

```
services/
 ├── document_classifier.py
 ├── embedding_service.py
 ├── ner_service.py
 ├── ocr_service.py
 └── storage_service.py
```

Cada arquivo resolve uma tarefa específica:

- `ocr_service.py` → lê texto de imagem/PDF
- `ner_service.py` → extrai entidades nomeadas
- `document_classifier.py` → classifica o tipo de documento
- `embedding_service.py` → gera vetores/embeddings
- `storage_service.py` → coordena a persistência (chamando a infraestrutura)

> 📌 Aqui acontece a **orquestração**: chamar domínio, infraestrutura e outros serviços na ordem certa para cumprir um caso de uso.

### 📦 `input/` e `output/`

```
services/
 ├── input/
 └── output/
```

Convenção comum para representar os dados que entram e saem de um caso de uso (DTOs):

- **input/** → dados que entram no sistema (DTOs, schemas de entrada)
- **output/** → respostas estruturadas (DTOs de retorno)

Exemplo:

```python
class UploadDocumentInput:
    file: bytes

class UploadDocumentOutput:
    document_type: str
```

> 💡 Separar `input`/`output` evita que os DTOs da aplicação fiquem acoplados aos schemas da API (camada externa) ou às entidades do domínio (camada interna).

---

## ⚙️ 3. `core/` — Configuração global

```
core/
 └── config.py
```

Aqui ficam:

- Variáveis de ambiente
- Paths/diretórios usados pelo sistema
- Configurações gerais
- Constantes

Exemplo:

```python
DB_PATH = "db/db.json"
MAX_SIZE_MB = 20
```

> 📌 Tudo que **não é regra de negócio**, mas afeta o sistema inteiro (configuração transversal).

> 💡 **Sugestão de evolução:** se o projeto crescer e precisar de autenticação, é comum adicionar um `core/security.py` para JWT, hashing de senha, etc. — mantendo a mesma filosofia de "infraestrutura transversal" separada da regra de negócio.

---

## 🧩 4. `domain/` — Regras puras (núcleo do sistema)

```
domain/
 └── models/
      ├── DocumentType.py
      └── user.py
```

Aqui fica o **núcleo do sistema**: entidades, enums e regras de negócio que não dependem de nada externo.

Exemplos:

- `DocumentType` (Enum com os tipos de documento)
- `User` (entidade de domínio)

> 📌 Aqui **NÃO entra FastAPI, banco de dados ou JSON**. Só lógica pura, testável sem nenhuma dependência externa.

Essa é a essência do DDD: o domínio representa o "mundo real" do negócio, independente de como ele é exposto (API) ou armazenado (banco).

---

## 🏗️ 5. `infrastructure/` — Parte técnica

```
infrastructure/
 ├── db/
 ├── http/
 └── persistence/
      ├── entity/
      └── repository/
```

Aqui fica tudo que depende de **tecnologia específica**:

- **`db/`** → implementação de acesso a dados (JSON, SQLite, PostgreSQL, etc.)
- **`http/`** → chamadas para APIs externas (clientes HTTP)
- **`persistence/entity/`** → entidades de banco de dados (ex: modelos do ORM, diferentes das entidades de domínio)
- **`persistence/repository/`** → implementação concreta dos repositórios

Exemplo:

```python
class JsonDocumentRepository:
    def save(self, doc):
        ...
```

> 📌 Aqui você **troca a tecnologia sem mexer no resto do sistema**. Se hoje você salva em JSON e quiser migrar para PostgreSQL, só a camada de infraestrutura muda — `domain` e `application` continuam intactos (desde que sigam interfaces/contratos bem definidos).

---

## 🚀 6. `main.py` — Ponto de entrada

```python
app = FastAPI()
app.include_router(routes)
```

> 📌 É aqui que tudo se junta: a aplicação FastAPI é criada e as rotas são registradas.

---

## 🧪 7. `test/` — Testes do sistema

- Testes **unitários** (services, domain)
- Testes de **integração** (API)
- **Mocks** de repositórios e serviços externos

A separação em camadas facilita muito os testes: é possível testar `domain` e `application` sem precisar de banco de dados real ou servidor HTTP rodando.

---

## 🧠 Resumo mental

```
API → chama Application → usa Domain → usa Infrastructure
```

| Camada | Conhece o quê? | Não conhece o quê? |
|---|---|---|
| `domain` | Nada externo | API, banco, FastAPI |
| `application` | `domain` | Detalhes de implementação de infraestrutura |
| `infrastructure` | `domain` (para implementar contratos) | Regras de negócio |
| `api` | `application` | Regras de negócio, banco |

---

## 🔄 Estrutura alternativa (padrão "services + repositories" mais simples)

Uma variação muito comum em projetos FastAPI menores ou que não seguem DDD estritamente é organizar por **tipo técnico** em vez de por camada de arquitetura:

```
meu_projeto/
├── app/
│   ├── __init__.py
│   ├── main.py              # ponto de entrada, cria a app
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py        # configurações (env vars, settings)
│   │   └── security.py      # autenticação, JWT, hashing
│   ├── api/
│   │   ├── __init__.py
│   │   ├── deps.py          # dependências injetadas (ex: get_db)
│   │   └── v1/
│   │       ├── __init__.py
│   │       └── routers/
│   │           ├── users.py
│   │           └── items.py
│   ├── models/              # modelos do banco (SQLAlchemy, etc.)
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── item.py
│   ├── schemas/             # validação/serialização (Pydantic)
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── item.py
│   ├── services/            # lógica de negócio
│   │   ├── __init__.py
│   │   └── user_service.py
│   ├── repositories/        # acesso a dados (queries)
│   │   ├── __init__.py
│   │   └── user_repository.py
│   └── db/
│       ├── __init__.py
│       ├── base.py          # Base do ORM
│       └── session.py       # conexão com banco
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_users.py
│   └── test_items.py
├── alembic/                 # migrations (se usar Alembic)
├── .env
├── .env.example
├── .gitignore
├── requirements.txt         # ou pyproject.toml
├── Dockerfile
├── docker-compose.yml
└── README.md
```

### Por que essa divisão?

- **`api/routers/`** — só cuida de rotas HTTP (request/response), sem lógica de negócio.
- **`schemas/`** — define o formato dos dados de entrada/saída (Pydantic), separado dos modelos do banco.
- **`models/`** — representa as tabelas do banco de dados.
- **`services/`** — onde fica a regra de negócio real. Isso facilita testar sem precisar de banco ou HTTP.
- **`repositories/`** — isola as queries, facilitando troca de banco ou mock em testes.
- **`core/config.py`** — centraliza configurações usando algo como `pydantic-settings`, lendo de variáveis de ambiente.

---

## ⚖️ Comparando as duas abordagens

| Aspecto | Estrutura atual (Clean Architecture + DDD) | Estrutura alternativa (services + repositories) |
|---|---|---|
| Critério de organização | Por **camada arquitetural** (api, application, domain, infrastructure) | Por **tipo técnico** (models, schemas, services, repositories) |
| Separação domínio x banco | Forte — `domain/models` é diferente de `infrastructure/persistence/entity` | Mais fraca — geralmente `models/` mistura entidade de banco e conceito de domínio |
| Curva de aprendizado | Maior, exige entender DDD/Clean Architecture | Menor, mais intuitiva para quem já usa FastAPI |
| Ideal para | Projetos médios/grandes, com regra de negócio complexa, múltiplas integrações (OCR, NER, embeddings, etc.) | Projetos pequenos/médios, CRUDs, MVPs |
| Troca de tecnologia (ex: JSON → Postgres) | Baixo impacto, isolado em `infrastructure` | Pode exigir mais ajustes, já que `models` está mais acoplado ao ORM |

Para o seu caso — um sistema que envolve OCR, NER, classificação de documentos e embeddings — a estrutura atual (Clean Architecture + DDD) tende a escalar melhor, porque cada serviço de IA/processamento fica isolado em `application/services`, e as regras de negócio (tipos de documento, validações) ficam protegidas em `domain`, sem se misturar com a parte técnica.

---

## 💡 Sugestões de evolução

1. **Interfaces/Contratos (Ports):** considere criar interfaces abstratas em `domain` (ex: `DocumentRepositoryInterface`) que são implementadas em `infrastructure/persistence/repository`. Isso reforça a inversão de dependência (a regra de negócio define o contrato, a infraestrutura o implementa).
2. **`api/deps.py`:** centralizar as dependências injetadas (ex: `get_db`, `get_current_user`) em um arquivo próprio dentro de `api/`, como na estrutura alternativa.
3. **Versionamento de API:** se o projeto crescer, vale adotar `api/v1/`, `api/v2/` para evitar breaking changes em clientes existentes.
4. **`core/security.py`:** separado de `config.py`, para autenticação, JWT e hashing, caso o projeto precise de autenticação no futuro.
5. **Migrations:** se migrar de JSON para um banco relacional, adicionar uma pasta `alembic/` (ou equivalente) para controle de versão do schema do banco.
