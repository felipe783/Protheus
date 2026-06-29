# Protheus - Obsidian Vault

Este vault documenta o projeto Protheus a partir do codigo presente em `E:\Downloads\!Faculdade\Protheus`.

## Entrada rapida

- [[arquitetura/visao-geral|Visao geral do sistema]]
- [[arquitetura/arquitetura|Arquitetura]]
- [[estrutura/estrutura-do-projeto|Estrutura do projeto]]
- [[fluxo/fluxo-de-execucao|Fluxo de execucao]]
- [[api/api-e-rotas|APIs e rotas]]
- [[setup/setup|Setup e execucao]]
- [[dependencias/dependencias|Dependencias]]
- [[glossary/glossary|Glossary]]

## Mapa do vault

### Arquitetura

- [[arquitetura/visao-geral]]
- [[arquitetura/arquitetura]]
- [[arquitetura/comunicacao-entre-camadas]]
- [[arquitetura/observacoes-tecnicas]]

### Modulos

- [[modulos/api]]
- [[modulos/application]]
- [[modulos/domain]]
- [[modulos/core]]
- [[modulos/infrastructure]]
- [[modulos/testes]]
- [[modulos/documentos-e-dados]]

### Fluxo

- [[fluxo/fluxo-de-execucao]]
- [[fluxo/fluxo-http-atual]]
- [[fluxo/fluxo-caso-de-uso-pretendido]]

### Referencia

- [[estrutura/estrutura-do-projeto]]
- [[api/api-e-rotas]]
- [[dependencias/dependencias]]
- [[setup/setup]]
- [[glossary/glossary]]

## Resumo tecnico

O Protheus e uma API Python baseada em FastAPI para receber documentos, detectar extensao, classificar tipo documental e extrair campos por regex. A organizacao segue uma tentativa de Clean Architecture/DDD, com separacao entre `api`, `application`, `domain`, `infrastructure` e `core`.

O ponto de entrada operacional e [[modulos/api|api/main.py]], que cria a instancia `FastAPI` e registra o router de documentos. A rota principal e `POST /document/extract`, implementada em [[api/api-e-rotas|ControllerDocument.py]].

