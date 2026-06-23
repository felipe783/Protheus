# Estrutura do Projeto — Clean Architecture + DDD + FastAPI

Essa estrutura é uma versão bem próxima de **Clean Architecture + DDD + FastAPI**, organizada por camadas.

## 📁 Estrutura geral

```
app/
 ├── api/
 ├── application/
 ├── core/
 ├── domain/
 ├── infrastructure/
 ├── main.py
 ├── test/
```

Isso separa o sistema em 4 níveis principais + entrada + testes.

---

## 🌐 1. `api/` (entrada do sistema)

Responsável por:

- Rotas FastAPI
- Requests e responses
- Dependências (`Depends`)

Exemplo:

```python
@router.post("/upload")
def upload(file: UploadFile):
    ...
```

> 📌 Aqui **não** fica regra de negócio.

---

## 🧠 2. `application/` (casos de uso)

Aqui fica o "cérebro operacional" do sistema.

```
services/
 ├── document_classifier.py
 ├── embedding_service.py
 ├── ner_service.py
 ├── ocr_service.py
 ├── storage_service.py
```

Isso significa que **cada arquivo resolve uma tarefa específica**:

- `ocr_service.py` → lê texto de imagem/pdf
- `ner_service.py` → extrai entidades
- `document_classifier.py` → classifica documento

> 📌 Aqui acontece a orquestração das regras.

### 📦 `input/` / `output/`

```
services/
 ├── input/
 ├── output/
```

Isso normalmente significa:

- **input** → dados que entram no sistema (DTOs, schemas)
- **output** → respostas estruturadas (DTOs de retorno)

Exemplo:

```python
class UploadDocumentInput:
    file: bytes
```

```python
class UploadDocumentOutput:
    document_type: str
```

---

## ⚙️ 3. `core/` (configuração global)

```
core/
 ├── config.py
```

Aqui fica:

- Variáveis de ambiente
- Paths
- Configs gerais
- Constantes

Exemplo:

```python
DB_PATH = "db/db.json"
MAX_SIZE_MB = 20
```

> 📌 Tudo que **não** é regra de negócio, mas afeta o sistema inteiro.

---

## 🧩 4. `domain/` (regras puras)

```
domain/
 ├── models/
 │    ├── DocumentType.py
 │    ├── user.py
```

Aqui fica o **núcleo do sistema**.

Exemplo:

- `DocumentType` (Enum)
- Entidades como `User`

> 📌 Aqui **não** entra FastAPI, banco ou JSON. Só lógica pura.

---

## 🏗️ 5. `infrastructure/` (parte técnica)

```
infrastructure/
 ├── db/
 ├── http/
 ├── persistence/
 │    ├── entity/
 │    ├── repository/
```

Aqui fica tudo que depende de tecnologia:

**`db/`**
- JSON
- SQLite
- PostgreSQL

**`http/`**
- Chamadas externas (APIs)

**`persistence/`**
- Entidades do banco
- Repositories (implementação)

Exemplo:

```python
class JsonDocumentRepository:
    def save(self, doc):
        ...
```

> 📌 Aqui você troca tecnologia sem mexer no resto do sistema.

---

## 🚀 6. `main.py`

Ponto de entrada da aplicação:

```python
app = FastAPI()
app.include_router(routes)
```

> 📌 Junta tudo.

---

## 🧪 7. `test/`

Testes do sistema:

- Unitários (services)
- Integração (API)
- Mocks

---

## 🧠 Resumo mental simples

Pensa assim:

```
API → chama Application → usa Domain → usa Infrastructure
```

### Fluxo:

```
Request (API)
   ↓
Use case (application)
   ↓
Regras puras (domain)
   ↓
Banco / JSON / API externa (infrastructure)
```
