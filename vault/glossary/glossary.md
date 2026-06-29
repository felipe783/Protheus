# Glossary

## API

Camada HTTP do sistema. No projeto, esta em [[modulos/api]].

## Application

Camada de orquestracao dos casos de uso. No projeto, esta em [[modulos/application]].

## Clean Architecture

Estilo arquitetural que separa dominio, casos de uso, interfaces externas e infraestrutura. O objetivo e proteger regra de negocio contra detalhes de framework, banco ou arquivos.

## Core

Modulo transversal com constantes, configuracoes, regex, keywords e logging. Ver [[modulos/core]].

## DANFE

Documento Auxiliar da Nota Fiscal Eletronica. No projeto aparece como tipo `DANFE_XML`.

## DDD

Domain-Driven Design. Abordagem que organiza o sistema ao redor do dominio e do vocabulário do negocio.

## Document

Entidade de dominio que representa um documento processado.

## DocumentExtension

Enum que representa extensoes de arquivo suportadas: `.pdf`, `.xml`, `.docx`, `.odt`.

## DocumentType

Enum que representa tipos documentais: CRLV-e, Cartao CNPJ, DANFE XML, Laudo, Contrato e Desconhecido.

## Entrypoint

Arquivo ou comando por onde a execucao comeca. O entrypoint principal e `api/main.py`.

## FastAPI

Framework Python usado para criar a API HTTP.

## FileReader

Interface de leitura de arquivos. Os leitores concretos ficam em [[modulos/infrastructure]].

## Infrastructure

Camada de detalhes tecnicos: leitores, banco JSON, logs e persistencia. Ver [[modulos/infrastructure]].

## Regex

Expressao regular usada para extrair campos especificos de texto. Os padroes ficam em `core/DocumentPatternsRegex.py`.

## Repository

Componente responsavel por persistir e recuperar entidades. No projeto existe `JsonDocumentRepository`.

## Uvicorn

Servidor ASGI usado para rodar a aplicacao FastAPI.

