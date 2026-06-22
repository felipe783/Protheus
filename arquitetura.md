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
│   │       ├── routers/
│   │       │   ├── users.py
│   │       │   └── items.py
│   │       └── __init__.py
│   ├── models/              # modelos do banco (SQLAlchemy, etc)
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
├── requirements.txt          # ou pyproject.toml
├── Dockerfile
├── docker-compose.yml
└── README.md

# Por que essa divisão?

**api/routers/** — só cuida de rotas HTTP (request/response), sem lógica de negócio.
**schemas/** — define o formato dos dados de entrada/saída (Pydantic), separado dos modelos do banco.
**models/** — representa as tabelas do banco de dados.
**services/** — onde fica a regra de negócio real. Isso facilita testar sem precisar de banco ou HTTP.
**repositories/** — isola as queries, facilitando troca de banco ou mock em testes.
**core/config.py** — centraliza configurações usando algo como pydantic-settings, lendo de variáveis de ambiente.