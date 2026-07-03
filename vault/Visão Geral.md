# Visão Geral do Sistema

O Protheus e um sistema de extração e classificação de documentos. O fluxo principal recebe um arquivo via API, identifica sua extração, tenta classificar o tipo documental e extrai campos usando padrões [Regex](https://regexr.com/).

## Finalidade

- Receber documentos
- Detectar extensões suportadas: `.pdf`, `.xml`, `.docx`, `.odt`.
- Classificar tipos como `danfe_xml`, `cartao_cnpj`, `crlv_e`,  ou `desconhecido`.
- Extrair dados estruturados quando existem padrões definidos.

## Entrada principal

- [[Main|api/main.py]] cria a aplicação FastAPI.
- [[Controller|api/ControllerDocument.py]] expõe HTTP
## Saída principal

## Camadas principais

- [[!Modulo API]]: borda HTTP.
- [[!Modulo Application]]: detectores, extrator e caso de uso.
- [[!Modulo Domain]]: enums, entidades e interfaces.
- [[!Modulo Core]]: constantes, regex, keywords, paths e logging.
- [[!Modulo Insfraestrutura]]: leitores de arquivos e persistencia JSON.


[[Dependencias]]




