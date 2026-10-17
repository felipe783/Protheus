---
projeto: Protheus
status: em desenvolvimento
stack: [Python, FastAPI, pypdf, python-docx, odfpy]
codigo: raiz do repositório (local: E:\Downloads\!Faculdade\Protheus)
atualizado: 2026-10-17
---
# Protheus

Sistema de **extração e classificação de documentos**. Recebe um arquivo via API, identifica a extensão, classifica o tipo documental por palavras-chave e extrai campos com [Regex](https://regexr.com/).

- **Código:** raiz deste repositório; a documentação fica em `vault/` (local: `E:\Downloads\!Faculdade\Protheus`)
- **Entrada:** `POST /document/extract` (upload `multipart/form-data`)
- **Saída:** `dict` com os campos extraídos; o documento também é salvo em `infrastructure/db/db.json`

## Status

| Funcionalidade | Estado |
|---|---|
| Upload e detecção de extensão (`.pdf`, `.xml`, `.docx`, `.odt`) | Implementado |
| Leitura de texto por extensão ([[Factory]] + readers) | Implementado |
| Classificação por palavras-chave ([[KeyWords]]) | Implementado |
| Extração Regex de CRLV-e, Cartão CNPJ e NF-e ([[Patterns]]) | Implementado |
| Persistência em JSON | Implementado (direto no controller) |
| Frontend estático (`FrontEnd/`) | Implementado |
| Extração de laudos e contratos ([[RF 02]]) | Planejado — classificados, sem padrões |
| Parsing estruturado do XML ([[RF 04]]) | Planejado — hoje é Regex sobre o texto |
| OCR para documentos escaneados ([[RF 04]], [[RF 05]]) | Planejado |
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

## Mapa das notas

- [[Visão Geral]]: visão resumida do sistema e das camadas.
- [[Resumo Principal]]: requisitos de upload, extração por formato e fluxo de processamento.
- [[Estrutura]]: árvore de pastas e arquivos.
- [[Dependencias]]: bibliotecas e instalação.
- Requisitos: [[RF 01]] · [[RF 02]] · [[RF 03]] · [[RF 04]] · [[RF 05]]
- Camadas:
  - [[!Modulo API]]: borda HTTP ([[Main]], [[Controller]]).
  - [[!Modulo Application]]: detectores, extrator, DTOs.
  - [[!Modulo Domain]]: enums, entidade, interfaces, factory.
  - [[!Modulo Core]]: keywords, regex, logging, paths.
  - [[!Modulo Insfraestrutura]]: readers e persistência JSON.

## Problemas conhecidos

Encontrados lendo o código em 2026-10-17. **Nada foi executado** para confirmar.

- O [[Controller]] orquestra tudo; o `ExtractDocumentUseCase` chama métodos inexistentes (`create`, `read`).
- O [[JSON Repository]] não é usado e tem imports de módulo em vez de classe.
- `JsonRepositoryDeps` usa um `DB_PATH` relativo próprio e ignora `core/dbPathConfig.py`. Por isso o `monkeypatch` dos testes não tem efeito, e `test_save_and_get_db` provavelmente grava no `db.json` real.
- `test_log.py` espera a mensagem "Salvo com sucesso", mas `save_db` não registra log: provavelmente falha.
- O sufixo do temporário fica `..pdf`, porque o valor do enum já tem o ponto.
- `print()` ativos na [[Factory]].
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
