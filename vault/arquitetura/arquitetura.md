# Arquitetura

O projeto usa uma estrutura inspirada em Clean Architecture e DDD.

```text
Cliente HTTP
  -> api
  -> application
  -> domain
  -> infrastructure
```

## Camadas

### API

Documentada em [[Main]].

Responsavel por protocolo HTTP, upload de arquivo e retorno da resposta. A API nao deveria conter regra de negocio pesada; ela deveria delegar para casos de uso.

### Application

Documentada em [[modulos/application]].

Contem a orquestracao do caso de uso:

- detectar extensao;
- ler conteudo;
- detectar tipo documental;
- extrair campos estruturados.

### Domain

Documentada em [[modulos/domain]].

Define conceitos estaveis:

- `documentType`;
- `documentExtension`;
- `Document`;
- contratos de `FileReader`, `DocumentRepository` e `DocumentExtractor`.

### Infrastructure

Documentada em [[modulos/infrastructure]].

Implementa detalhes tecnicos:

- leitores de PDF, XML, DOCX e ODT;
- persistencia em JSON;
- entidade de persistencia.

### Core

Documentada em [[modulos/core]].

Agrupa configuracoes e constantes transversais:

- regex de extracao;
- keywords de classificacao;
- caminho do banco JSON;
- configuracao de logs.

## Regra esperada de dependencia

Em Clean Architecture, as regras de dominio devem permanecer independentes de FastAPI, banco, arquivos e bibliotecas externas. O fluxo desejado e:

```text
api -> application -> domain
infrastructure -> domain
core -> usado como suporte transversal
```

O codigo atual ainda tem alguns acoplamentos e inconsistencias, listados em [[arquitetura/observacoes-tecnicas]].

