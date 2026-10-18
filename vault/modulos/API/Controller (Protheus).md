# Sobre o Arquivo

O Arquivo `controller` é a **porta de entrada HTTP** do upload. Desde 2026-10-18 ele não orquestra mais o fluxo: só recebe o arquivo, monta o caso de uso com o repositório concreto e devolve o resultado. A orquestração (temporário → factory → reader → detector → extractor → `Document` → JSON) fica no `ExtractDocumentUseCase` (ver [[!Modulo Application (Protheus)|!Modulo Application]]).

Responsabilidades:
- criar o `Endpoint`
- Receber os Arquivo que foi dado Upload pelo Usuário
- Escolher a implementação do repositório ([[JSON Repository]]) e entregá-la ao caso de uso
- Retornar a resposta HTTP
# Funcionalidades

## Criação EndPoint:

````python
	documentController = APIRouter(
		prefix="/document",
		tags=["document"]
	)
````
## Upload e delegação ao caso de uso

- A API recebe o arquivo via FastAPI, lê os bytes e passa conteúdo e nome do arquivo para o caso de uso. O retorno é o `dict` com os campos extraídos (o mesmo de antes da migração).
- O `JsonDocumentRepository` é criado **aqui**, e não dentro da `application`: assim a camada Application depende só da interface `DocumentRepository` e não importa diretamente a persistência da `infrastructure` (a ressalva é a Factory, que ainda importa os readers).
- O import de `core.Logs.LogUploadConfig` continua no controller: é ele que executa o `logging.basicConfig` e direciona os logs para `infrastructure/logs/uploads_logs.log`.

````python
@documentController.post("/extract")
async def extract_document(file: UploadFile = File(...)):

    content = await file.read()
    useCase = ExtractDocumentUseCase(JsonDocumentRepository())
    return useCase.execute(file_content=content, filename=file.filename)
````

> [!note] Verificado em 2026-10-18
> Com `uvicorn`, `POST /document/extract` com `test.xml`, `test2.pdf` e `test3.odt` retornou HTTP 200. Os `dict`s e os registros gravados (chaves, `type`/`extension` como texto) ficaram iguais aos que o código anterior já tinha salvo no `db.json`.

---
**Projeto Pai:** [[_Protheus]] · **Módulo:** [[!Modulo API (Protheus)|!Modulo API]]
