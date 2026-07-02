# Visão Geral do Sistema

O Protheus e um sistema de extração e classificação de documentos. O fluxo principal recebe um arquivo via API, identifica sua extração, tenta classificar o tipo documental e extrai campos usando padrões [Regex](https://regexr.com/).

## Finalidade

- Receber documentos
- Detectar extensões suportadas: `.pdf`, `.xml`, `.docx`, `.odt`.
- Classificar tipos como `danfe_xml`, `cartao_cnpj`, `crlv_e`,  ou `desconhecido`.
- Extrair dados estruturados quando existem padrões definidos.

## Entrada principal

- [[Main|api/main.py]] cria a aplicação FastAPI.
- [[api/api-e-rotas|api/routers/ControllerDocument.py]] expõe HTTP

## Camadas principais

- [[Main]]: borda HTTP.
- [[modulos/application]]: detectores, extrator e caso de uso.
- [[modulos/domain]]: enums, entidades e interfaces.
- [[modulos/infrastructure]]: leitores de arquivos e persistencia JSON.
- [[modulos/core]]: constantes, regex, keywords, paths e logging.

## Dados processados

O projeto inclui arquivos de exemplo na raiz:

- `test.xml`
- `documento_empresa.pdf`
- `documento_empresa.odt`

Esses arquivos parecem servir como amostras manuais para validar leitura e extracao. Veja [[modulos/documentos-e-dados]].

## Observacao importante

Ha uma diferenca entre o fluxo HTTP atual e o fluxo de caso de uso pretendido. A rota atual decodifica o upload diretamente como UTF-8, enquanto [[Fluxo caso de Uso]] sugere um desenho com `FileReaderFactory` e leitores por extensao.

Detalhes em [[arquitetura/observacoes-tecnicas]].

