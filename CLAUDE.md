# CLAUDE.md — Protheus

API **FastAPI** de **extração e classificação de documentos**. Recebe um arquivo (`.pdf`, `.xml`, `.docx`, `.odt`), extrai o texto com o reader da extensão, classifica o tipo (CRLV-e, Cartão CNPJ, NF-e/DANFE…) por palavras-chave e extrai campos com **Regex**. O resultado é persistido num arquivo JSON. A organização segue **Clean Architecture + DDD** (`api` → `application` → `domain` ← `infrastructure`, com `core` transversal).

O perfil do autor e as preferências gerais estão no `CLAUDE.md` de `!Faculdade`. Este arquivo trata só do que é específico deste repositório.

## Documentação (fonte de verdade)

O índice abaixo é carregado em toda sessão. As notas detalhadas ficam em `vault/` e devem ser lidas **sob demanda**:

@vault/_Protheus.md

| Assunto | Nota |
|---|---|
| Fluxo completo do upload até o JSON | `vault/Requisitos/Resumo Principal (Protheus).md` |
| Requisitos funcionais | `vault/Requisitos/Funcionais/PT-RF 01.md` … `PT-RF 05.md` |
| Rota e orquestração | `vault/modulos/API/Controller (Protheus).md`, `Main (Protheus).md` |
| Detecção de tipo e extração Regex | `vault/modulos/Application/Extrator e Detector.md` |
| Palavras-chave e padrões | `vault/modulos/Core/KeyWords (Protheus).md`, `Patterns (Protheus).md` |
| Enums, entidade, factory, interfaces | `vault/modulos/Domain/` |
| Readers e persistência JSON | `vault/modulos/Infraestrutura/` |

Há também textos de arquitetura em `docs/` (guias genéricos de Clean Architecture + DDD). Para o estado real, o `vault/` prevalece.

Conceitos transversais (camadas, caminhos, testes, persistência, erros e logs…), com aprendizados deste e de outros projetos: `E:/Downloads/!Faculdade/Contexto Projetos/Conhecimento/_Conhecimento.md`. Leia sob demanda, quando a tarefa tocar o assunto.

## Mapa do código

- `api/main.py`: cria o `FastAPI`, configura o CORS (`localhost:5500` e `127.0.0.1:5500`) e registra o router.
- `api/routers/ControllerDocument.py`: `POST /document/extract`. Lê o upload e chama `ExtractDocumentUseCase(JsonDocumentRepository()).execute(...)`.
- `application/`: `DocumentExtensionDetector`, `DocumentTypeDetector`, `DocumentExtractor`, DTOs em `input/` e `output/`, e `ExtractDocumentUseCase.py`, que orquestra o fluxo (temporário → factory → reader → detector → extractor → `Document` → `repository.save`) e recebe o `DocumentRepository` no construtor.
- `domain/models/`: enums `documentType` e `documentExtension`, `Document`, `DocumentUUID`, `FileReaderFactory`. `domain/interfaces/`: `FileReader`, `DocumentRepository`, `DocumentExtractor`.
- `infrastructure/readers/`: `PdfReader` (pypdf), `DocxReader` (python-docx), `OdtReader` (odfpy), `XmlReader` (decodifica bytes; **não** faz parse).
- `infrastructure/persistence/`: `DocumentEntity`, `JsonRepositoryDeps` (`get_db`/`save_db`, com caminho de `core/dbPathConfig.py`) e `JsonDocumentRepository` (usado pelo caso de uso).
- `core/`: `DocumentKeyWords.py`, `DocumentPatternsRegex.py`, `Logs/LogUploadConfig.py`, `dbPathConfig.py` (caminho absoluto do `db.json`).
- `FrontEnd/`: HTML/JS estático que chama `http://localhost:8000/document/extract`.
- `test/`: `test_db.py`, `test_log.py`, `test_use_case.py`.

## Comandos

Tudo a partir da **raiz** do repositório: os imports são absolutos (`from domain.models...`) e o caminho do log é relativo ao diretório atual.

```powershell
.\.venv\Scripts\Activate.ps1
pip install -r requiriments.txt          # o nome do arquivo tem esse erro de digitação

python -m uvicorn api.main:app --reload  # API em http://127.0.0.1:8000/docs
cd FrontEnd; python -m http.server 5500  # front em http://localhost:5500 (outro terminal)

python -m pytest -v                      # testes
```

**Peça autorização antes de instalar dependências.** O que a `.venv` tinha na última verificação está no "Como rodar" do índice.

## Regras deste projeto

- **Respeite as camadas**: `domain` não importa `infrastructure`, `application` nem `api`. Hoje a `FileReaderFactory` (em `domain/models`) importa os readers de `infrastructure`, o que é uma violação já conhecida. Não a replique, e aponte-a ao mexer ali.
- **Novo formato de arquivo** = membro em `documentExtension` (com o ponto, ex. `".rtf"`) + reader em `infrastructure/readers/` implementando `FileReader.extract(path) -> str` + `case` na `FileReaderFactory` + dependência no `requiriments.txt`.
- **Novo tipo de documento** = membro em `documentType` + lista em `KEY_WORDS` + dicionário em `DOCUMENT_PATTERNS`. Sem padrões, o tipo é classificado mas a extração retorna `{}` (é o caso atual de `LAUDO` e `CONTRATO`).
- A classificação exige **≥ 3 palavras-chave** encontradas, senão o tipo é `DESCONHECIDO`. O texto é comparado em minúsculas; a extração Regex usa o texto em **maiúsculas**, exceto no `DANFE_XML`, que preserva o original (as tags XML diferenciam maiúsculas).
- Os Regex usam `re.DOTALL | re.MULTILINE` e só o **grupo 1** é capturado. Ao escrever um padrão, garanta exatamente um grupo de captura com o valor.
- **Persistência**: o arquivo é `infrastructure/db/db.json` (caminho absoluto em `core/dbPathConfig.py`) e o log é `infrastructure/logs/uploads_logs.log` (relativo ao diretório atual). Não teste gravando no `db.json` real: faça `monkeypatch.setattr("core.dbPathConfig.DB_PATH", tmp_path / "db.json")`, o que só funciona porque `JsonRepositoryDeps` lê `dbPathConfig.DB_PATH` na hora da chamada.
- A orquestração fica no `ExtractDocumentUseCase`. O controller só monta as dependências: a `application` não importa diretamente a persistência da `infrastructure` (a ressalva é a Factory, que ainda importa os readers).
- O XML **não** é parseado com `ElementTree`: é Regex sobre o texto. O parse estruturado é requisito (RF 04) ainda não implementado. Não descreva o comportamento como se já existisse.

## Armadilhas conhecidas

Estão em **Problemas conhecidos** do índice importado acima (`vault/_Protheus.md`), que é a única lista mantida.

## Manter a documentação

Ao alterar comportamento, atualize na mesma tarefa:
1. `vault/_Protheus.md`: **Status**, **Problemas conhecidos** e `Atualizado` no frontmatter.
2. A nota do módulo afetado (tabela acima) e, se mudar o fluxo, o `Resumo Principal (Protheus)`.
3. `vault/Estrutura (Protheus).md`, se arquivos forem criados, movidos ou removidos.

Convenções do vault (o mesmo do Obsidian em `Contexto Projetos/Protheus`, via junction):
- Frontmatter: siga a tabela de **Convenções** em `E:/Downloads/!Faculdade/Contexto Projetos/Contexto Geral.md`, que é a única definição (`Tipo`, `Status` controlado, `Codigo` relativo) e tem templates em `_templates/`.
- Nomes de nota únicos no vault inteiro: notas genéricas levam `(Protheus)`; requisitos usam `PT-RF NN`.
- Notas de módulo novas partem do template `Template - Modulo` (H1 = nome da nota, seções em H2, callouts `> [!warning]` para divergências). As notas antigas usam `# Sobre o Arquivo` / `# Funcionalidades`; não é preciso convertê-las.
- Separe o que foi **executado** do que foi **lido no código**, com data.
