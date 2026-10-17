# Protheus — Extração e Classificação de Documentos

API em **FastAPI** que recebe um documento (`.pdf`, `.xml`, `.docx` ou `.odt`), extrai o texto e o classifica por palavras-chave como **CRLV-e**, **Cartão CNPJ** ou **NF-e/DANFE**. Depois extrai os campos com **expressões regulares**. O resultado volta na resposta HTTP e também é salvo num arquivo JSON local.

O código segue **Clean Architecture + DDD**:

| Camada | Pasta | Papel |
|---|---|---|
| API | `api/` | aplicação FastAPI, CORS e rota `POST /document/extract` |
| Application | `application/` | detecção de extensão e de tipo, extração por Regex, DTOs |
| Domain | `domain/` | enums `documentType`/`documentExtension`, entidade `Document`, interfaces, `FileReaderFactory` |
| Infrastructure | `infrastructure/` | readers por formato (pypdf, python-docx, odfpy, XML) e persistência JSON |
| Core | `core/` | palavras-chave, padrões Regex, log e caminhos |
| Frontend | `FrontEnd/` | página HTML/JS estática para enviar arquivos |

Fluxo: **upload → reader da extensão → texto → classificação por palavras-chave → Regex do tipo → `dict` de campos → `infrastructure/db/db.json`**.

## Pré-requisitos

- Python 3.12 (com `.venv` na raiz)
- Nenhum serviço externo: a persistência é um arquivo JSON

## Configuração local

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requiriments.txt
```

> O arquivo de dependências se chama `requiriments.txt`, com esse erro de digitação. Ele traz `fastapi`, `uvicorn`, `python-multipart`, `python-docx`, `odfpy` e `pypdf`.

Não há variáveis de ambiente. O banco (`infrastructure/db/db.json`) e o log (`infrastructure/logs/uploads_logs.log`) usam **caminhos relativos ao diretório atual**, então rode tudo **a partir da raiz do repositório**.

## Execução

```powershell
# API — documentação interativa em http://127.0.0.1:8000/docs
python -m uvicorn api.main:app --reload

# Frontend — em outro terminal, abre em http://localhost:5500
cd FrontEnd
python -m http.server 5500
```

O CORS da API libera apenas `http://localhost:5500` e `http://127.0.0.1:5500`.

## Uso da API

```bash
curl -F "file=@test2.pdf" http://127.0.0.1:8000/document/extract
```

- **Requisição:** `multipart/form-data` com o arquivo no campo `file`.
- **Resposta:** um objeto com os campos extraídos do tipo detectado (ex.: `chave_acesso`, `numero_nota` para NF-e; `cnpj`, `nome_fantasia` para Cartão CNPJ; `placa`, `renavam` para CRLV-e). Campos não encontrados vêm como `null`.
- **Tipos sem padrões:** um tipo sem padrões Regex (laudo, contrato) ou não reconhecido (`desconhecido`) retorna `{}`.
- **Arquivos de exemplo:** `test.xml`, `test2.pdf` e `test3.odt`, na raiz.

## Testes

```powershell
pip install pytest
python -m pytest -v
```

Os testes ficam em `test/` (`test_db.py`, `test_log.py`) e cobrem a persistência JSON e o log.

## Solução de problemas

| Sintoma | Causa provável |
|---|---|
| `ModuleNotFoundError: No module named 'api'` / `'domain'` | O Uvicorn foi iniciado fora da raiz do repositório |
| Erro de CORS no navegador | O frontend não está em `localhost:5500` ou `127.0.0.1:5500` |
| `500` ao enviar um arquivo | Extensão fora de `.pdf/.xml/.docx/.odt`: o `ValueError` não é convertido em resposta 4xx |
| Resposta `{}` | Tipo não reconhecido (menos de 3 palavras-chave) ou tipo sem padrões Regex |
| `db.json`/log criados em outra pasta | Os caminhos são relativos ao diretório de onde a API foi iniciada |
| PDF escaneado sem campos | O `pypdf` só lê texto embutido; não há OCR |

## Documentação

A documentação completa do projeto está em [`vault/_Protheus.md`](vault/_Protheus.md). Consulte esse arquivo como ponto de entrada para toda a documentação do projeto.
