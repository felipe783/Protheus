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
Atualizado: 2026-10-18
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
| Persistência em JSON | Implementado (via [[JSON Repository]]) |
| Frontend estático (`FrontEnd/`) | Implementado |
| Extração de laudos e contratos ([[PT-RF 02|RF 02]]) | Planejado — classificados, sem padrões |
| Parsing estruturado do XML ([[PT-RF 04|RF 04]]) | Planejado — hoje é Regex sobre o texto |
| OCR para documentos escaneados ([[PT-RF 04|RF 04]], [[PT-RF 05|RF 05]]) | Planejado |
| Caso de uso na camada Application (`ExtractDocumentUseCase`) | Implementado — orquestra o fluxo desde 2026-10-18 |
| Testes automatizados (`test/`) | Implementado — 5 testes passando em 2026-10-18, com banco isolado |
| IA para documentos não padronizados / resumos | Ideia futura |

## Como rodar

```bash
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requiriments.txt
python -m uvicorn api.main:app --reload   # API em http://127.0.0.1:8000/docs
cd FrontEnd && python -m http.server 5500 # Front em http://localhost:5500
python -m pytest -v                       # testes
```

> Rode a partir da raiz do projeto: os imports são absolutos e o caminho do **log** é relativo. O banco usa o caminho absoluto de `core/dbPathConfig.py`.
> Em 2026-10-18 a `.venv` (Python 3.12) tinha `fastapi 0.138`, `uvicorn 0.49`, `python-multipart`, `python-docx`, `odfpy`, `pypdf 6.14` e `pytest 9.1` (adicionado ao `requiriments.txt`).

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
  - [[!Modulo Infraestrutura (Protheus)|!Modulo Infraestrutura]]: readers e persistência JSON.

## Problemas conhecidos

Revisados em 2026-10-18.

- `requiriments.txt` tem o nome com erro de digitação.
- A [[Factory (Protheus)|Factory]] fica em `domain/models`, mas importa os readers de `infrastructure` (violação de camadas).
- `JsonDocumentRepository.getAll` não reconverte `created_in`/`type`/`extension` (voltam como `str`). Não é usado por nenhuma rota.
- O caminho do log (`core/Logs/LogUploadConfig.py`) ainda é relativo ao diretório de execução.
- Extensão não suportada levanta `ValueError` sem tratamento, então a API responde 500 em vez de 4xx. Lido no código, não testado.

> [!success] Corrigidos em 2026-10-18 (verificado com `pytest` e `uvicorn`)
> - Orquestração movida do [[Controller (Protheus)|Controller]] para o `ExtractDocumentUseCase`, já com `FileReaderFactory.get` e `reader.extract(path)`. O endpoint retorna o mesmo `dict`.
> - [[JSON Repository]] e [[Entity (Protheus)|DocumentEntity]] importavam módulos em vez de classes (`TypeError` ao carregar). Corrigidos, e o repositório agora é usado no fluxo.
> - `JsonRepositoryDeps` lê o `DB_PATH` de `core/dbPathConfig.py` a cada chamada. Antes, os testes gravavam no `db.json` real: o baseline sobrescreveu o banco, que foi restaurado pelo git.
> - `save_db` registra `INFO` "Salvo com sucesso": o teste estava certo e faltava o log no código.
> - O sufixo do temporário passou a ser `extension.value` (`.pdf`, e não `..pdf`). Os `print()` da Factory viraram `logging.debug`.

## Decisões

- **Regex em vez de IA** para documentos de layout fixo (CRLV-e, CNPJ, NF-e): é determinístico, barato e fácil de testar.
- **Persistência em JSON** em vez de banco: é simples para a fase atual. O contrato `DocumentRepository` permite trocar depois.
- **Readers por extensão via Factory**: para adicionar um formato, basta criar o reader e um `case` novo.

## Próximos passos sugeridos

1. Implementar os padrões de laudo e contrato, ou removê-los do escopo.
2. Responder 4xx para extensão não suportada (hoje é 500).
3. Tirar da `domain` o import dos readers (injetar a factory ou movê-la para `infrastructure`).
