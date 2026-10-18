---
Tipo: projeto
Projeto: Protheus
Status: ativo
Stack:
  - Python
  - FastAPI
  - pypdf
  - python-docx
  - odfpy
Codigo: "Protheus"
Repositorio: "https://github.com/felipe783/Protheus"
Atualizado: 2026-10-17
---
# Protheus

Sistema de **extração e classificação de documentos**. Recebe um arquivo via API, identifica a extensão, classifica o tipo documental por palavras-chave e extrai campos com [Regex](https://regexr.com/).

- **Código:** raiz deste repositório; a documentação fica em `vault/`
- **Entrada:** `POST /document/extract` (upload `multipart/form-data`)
- **Saída:** `dict` com os campos extraídos; o documento também é salvo em `infrastructure/db/db.json`

## Status

| Funcionalidade | Estado |
|---|---|
| Upload e detecção de extensão (`.pdf`, `.xml`, `.docx`, `.odt`) | Implementado |
| Leitura de texto por extensão ([[Factory (Protheus)|Factory]] + readers) | Implementado |
| Classificação por palavras-chave ([[KeyWords (Protheus)|KeyWords]]) | Implementado |
| Extração Regex de CRLV-e, Cartão CNPJ e NF-e ([[Patterns (Protheus)|Patterns]]) | Implementado |
| Persistência em JSON | Implementado (direto no controller) |
| Frontend estático (`FrontEnd/`) | Implementado |
| Extração de laudos e contratos ([[PT-RF 02|RF 02]]) | Planejado — classificados, sem padrões |
| Parsing estruturado do XML ([[PT-RF 04|RF 04]]) | Planejado — hoje é Regex sobre o texto |
| OCR para documentos escaneados ([[PT-RF 04|RF 04]], [[PT-RF 05|RF 05]]) | Planejado |
| Caso de uso na camada Application | Existe, mas não é usado e está quebrado |
| IA para documentos não padronizados / resumos | Ideia futura |

## Como rodar

```bash
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requiriments.txt
python -m uvicorn api.main:app --reload   # API em http://127.0.0.1:8000/docs
cd FrontEnd && python -m http.server 5500 # Front em http://localhost:5500
python -m pytest -v                       # testes
```

> Os caminhos do banco e do log são **relativos**: rode a API a partir da raiz do projeto.
> Em 2026-10-17 a `.venv` tinha `fastapi 0.138`, `uvicorn 0.49`, `python-multipart`, `python-docx`, `odfpy` e `pypdf 6.14`, mas **não** tinha `pytest`; os testes nunca foram executados.

## Mapa das notas

- [[Visão Geral (Protheus)|Visão Geral]]: visão resumida do sistema e das camadas.
- [[Resumo Principal (Protheus)|Resumo Principal]]: requisitos de upload, extração por formato e fluxo de processamento.
- [[Estrutura (Protheus)|Estrutura]]: árvore de pastas e arquivos.
- [[Dependencias (Protheus)|Dependencias]]: bibliotecas e instalação.
- Requisitos: [[PT-RF 01|RF 01]] · [[PT-RF 02|RF 02]] · [[PT-RF 03|RF 03]] · [[PT-RF 04|RF 04]] · [[PT-RF 05|RF 05]]
- Camadas:
  - [[!Modulo API (Protheus)|!Modulo API]]: borda HTTP ([[Main (Protheus)|Main]], [[Controller (Protheus)|Controller]]).
  - [[!Modulo Application (Protheus)|!Modulo Application]]: detectores, extrator, DTOs.
  - [[!Modulo Domain (Protheus)|!Modulo Domain]]: enums, entidade, interfaces, factory.
  - [[!Modulo Core (Protheus)|!Modulo Core]]: keywords, regex, logging, paths.
  - [[!Modulo Infraestrutura (Protheus)|!Modulo Insfraestrutura]]: readers e persistência JSON.

## Problemas conhecidos

Encontrados lendo o código em 2026-10-17. **Nada foi executado** para confirmar.

- O [[Controller (Protheus)|Controller]] orquestra tudo; o `ExtractDocumentUseCase` chama `FileReaderFactory.create(...)` e `reader.read(...)`, que não existem; os reais são `get` e `extract`.
- O [[JSON Repository]] não é usado e tem imports de módulo em vez de classe.
- `JsonRepositoryDeps` usa um `DB_PATH` relativo próprio e ignora `core/dbPathConfig.py`. Por isso o `monkeypatch` dos testes não tem efeito, e `test_save_and_get_db` provavelmente grava no `db.json` real.
- `test_log.py` espera a mensagem "Salvo com sucesso", mas `save_db` não registra log: provavelmente falha.
- O sufixo do temporário (`suffix=f".{extension.value}"` no controller) fica `..pdf`, porque o valor do enum já tem o ponto.
- `print()` ativos na `FileReaderFactory` ([[Factory (Protheus)|Factory]]).
- `requiriments.txt` tem o nome com erro de digitação.

## Decisões

- **Regex em vez de IA** para documentos de layout fixo (CRLV-e, CNPJ, NF-e): é determinístico, barato e fácil de testar.
- **Persistência em JSON** em vez de banco: é simples para a fase atual. O contrato `DocumentRepository` permite trocar depois.
- **Readers por extensão via Factory**: para adicionar um formato, basta criar o reader e um `case` novo.

## Próximos passos sugeridos

1. Mover a orquestração do controller para o `ExtractDocumentUseCase`, corrigindo os métodos.
2. Usar o `JsonDocumentRepository` no fluxo e centralizar o `DB_PATH` em `core/dbPathConfig.py`.
3. Corrigir os testes para que isolem o banco de verdade.
4. Implementar os padrões de laudo e contrato, ou removê-los do escopo.
