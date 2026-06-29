# Setup e Execucao

## Ambiente

O projeto possui uma venv local:

```text
.venv/
```

Ativacao no PowerShell:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
& .\.venv\Scripts\Activate.ps1
```

## Instalar dependencias

Nao ha manifesto de dependencias no projeto. Com base nos imports, o ambiente precisa de:

```powershell
pip install fastapi uvicorn pypdf python-docx odfpy pytest
```

## Rodar API

Na raiz do projeto:

```powershell
python -m uvicorn api.main:app --reload
```

Depois acesse:

```text
http://127.0.0.1:8000/docs
```

## Rodar testes

```powershell
python -m pytest -v
```

## Arquivos importantes para execucao

- [[modulos/api|api/main.py]]
- [[api/api-e-rotas|api/routers/ControllerDocument.py]]
- [[modulos/application|application/DocumentExtractor.py]]
- [[modulos/core|core/DocumentPatternsRegex.py]]
- [[modulos/core|core/DocumentKeyWords.py]]

