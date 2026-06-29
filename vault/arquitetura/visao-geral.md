# Visao Geral do Sistema

O Protheus e um sistema de extracao e classificacao de documentos. O fluxo principal recebe um arquivo via API, identifica sua extensao, tenta classificar o tipo documental e extrai campos usando padroes regex.

## Finalidade

- Receber documentos fiscais ou cadastrais.
- Detectar extensoes suportadas: `.pdf`, `.xml`, `.docx`, `.odt`.
- Classificar tipos como `danfe_xml`, `cartao_cnpj`, `crlv_e`, `laudo`, `contrato` ou `desconhecido`.
- Extrair dados estruturados quando existem padroes definidos.

## Entrada principal

- [[modulos/api|api/main.py]] cria a aplicacao FastAPI.
- [[api/api-e-rotas|api/routers/ControllerDocument.py]] expoe `POST /document/extract`.

## Camadas principais

- [[modulos/api]]: borda HTTP.
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

Ha uma diferenca entre o fluxo HTTP atual e o fluxo de caso de uso pretendido. A rota atual decodifica o upload diretamente como UTF-8, enquanto [[fluxo/fluxo-caso-de-uso-pretendido]] sugere um desenho com `FileReaderFactory` e leitores por extensao.

Detalhes em [[arquitetura/observacoes-tecnicas]].

