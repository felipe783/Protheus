# CLAUDE.md — Protheus

API **FastAPI** de **extração e classificação de documentos**. Recebe um arquivo (`.pdf`, `.xml`, `.docx`, `.odt`), extrai o texto com o reader da extensão, classifica o tipo (CRLV-e, Cartão CNPJ, NF-e/DANFE…) por palavras-chave e extrai campos com **Regex**. O resultado é persistido num arquivo JSON. A organização segue **Clean Architecture + DDD** (`api` → `application` → `domain` ← `infrastructure`, com `core` transversal).

O perfil do autor e as preferências gerais estão no `CLAUDE.md` de `!Faculdade`. Este arquivo trata só do que é específico deste repositório.

## Documentação (fonte de verdade)

O índice abaixo é carregado em toda sessão. As notas detalhadas ficam em `vault/` e devem ser lidas **sob demanda**:

@vault/_Protheus.md

| Assunto | Nota |
|---|---|
| Fluxo completo do upload até o JSON | `vault/Requisitos/Resumo Principal.md` |
| Requisitos funcionais | `vault/Requisitos/Funcionais/RF 01.md` … `RF 05.md` |
| Rota e orquestração | `vault/Modulos/API/Controller.md`, `Main.md` |
| Detecção de tipo e extração Regex | `vault/Modulos/Application/Extrator e Detector.md` |
| Palavras-chave e padrões | `vault/Modulos/Core/KeyWords.md`, `Patterns.md` |
| Enums, entidade, factory, interfaces | `vault/Modulos/Domain/` |
| Readers e persistência JSON | `vault/Modulos/Infraestrutura/` |

Há também textos de arquitetura em `docs/` (guias genéricos de Clean Architecture + DDD). Para o estado real, o `vault/` prevalece.

Conceitos transversais (camadas, caminhos, testes, persistência, erros e logs…), com aprendizados deste e de outros projetos: `E:/Downloads/!Faculdade/Contexto Projetos/Conhecimento/_Conhecimento.md`. Leia sob demanda, quando a tarefa tocar o assunto.

## Mapa do código

- `api/main.py`: cria o `FastAPI`, configura o CORS (`localhost:5500` e `127.0.0.1:5500`) e registra o router.
- `api/routers/ControllerDocument.py`: `POST /document/extract`. **Hoje orquestra todo o fluxo** (temporário → factory → reader → detector → extractor → `Document` → JSON).
- `application/`: `DocumentExtensionDetector`, `DocumentTypeDetector`, `DocumentExtractor`, DTOs em `input/` e `output/`, e `ExtractDocumentUseCase.py` (**não usado e quebrado**).
- `domain/models/`: enums `documentType` e `documentExtension`, `Document`, `DocumentUUID`, `FileReaderFactory`. `domain/interfaces/`: `FileReader`, `DocumentRepository`, `DocumentExtractor`.
- `infrastructure/readers/`: `PdfReader` (pypdf), `DocxReader` (python-docx), `OdtReader` (odfpy), `XmlReader` (decodifica bytes; **não** faz parse).
- `infrastructure/persistence/`: `DocumentEntity`, `JsonRepositoryDeps` (`get_db`/`save_db`) e `JsonDocumentRepository` (**não usado**).
- `core/`: `DocumentKeyWords.py`, `DocumentPatternsRegex.py`, `Logs/LogUploadConfig.py`, `dbPathConfig.py` (não importado pelo repositório JSON).
- `FrontEnd/`: HTML/JS estático que chama `http://localhost:8000/document/extract`.
- `test/`: `test_db.py`, `test_log.py`.

## Comandos

Tudo a partir da **raiz** do repositório: os imports são absolutos (`from domain.models...`) e os caminhos do banco e do log são relativos ao diretório atual.

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
- **Persistência**: o arquivo é `infrastructure/db/db.json` e o log é `infrastructure/logs/uploads_logs.log`, ambos relativos ao diretório atual. Não teste gravando no `db.json` real.
- **Não reescreva o controller inteiro** sem pedido: a migração da orquestração para o `ExtractDocumentUseCase` é uma tarefa planejada e própria.
- O XML **não** é parseado com `ElementTree`: é Regex sobre o texto. O parse estruturado é requisito (RF 04) ainda não implementado. Não descreva o comportamento como se já existisse.

## Armadilhas conhecidas

Estão em **Problemas conhecidos** do índice importado acima (`vault/_Protheus.md`), que é a única lista mantida.

## Manter a documentação

Ao alterar comportamento, atualize na mesma tarefa:
1. `vault/_Protheus.md`: **Status**, **Problemas conhecidos** e `Atualizado` no frontmatter.
2. A nota do módulo afetado (tabela acima) e, se mudar o fluxo, o `Resumo Principal`.
3. `vault/Estrutura.md`, se arquivos forem criados, movidos ou removidos.

Convenções do vault (o mesmo do Obsidian em `Contexto Projetos/Protheus`, via junction):
- Frontmatter: siga a tabela de **Convenções** em `E:/Downloads/!Faculdade/Contexto Projetos/Contexto Geral.md`, que é a única definição (`Tipo`, `Status` controlado, `Codigo` relativo) e tem templates em `_templates/`.
- As notas do Protheus usam nomes curtos (`Main`, `Controller`, `Factory`…). Notas novas não podem repetir nomes já usados em outros projetos do vault.
- Formato das notas de módulo: `# Sobre o Arquivo` → `Responsabilidade:` → `# Funcionalidade(s)` com trechos ````python e callouts `> [!warning]` para divergências.
- Separe o que foi **executado** do que foi **lido no código**, com data.
