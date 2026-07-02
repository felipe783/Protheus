# Documentos e Dados

O projeto contem dados e arquivos de exemplo usados como insumo manual.

## Arquivos de exemplo

### `test.xml`

Arquivo XML de exemplo. Deve ser util para validar:

- leitura de XML;
- deteccao de NF-e/DANFE XML;
- regex de `NFE_PATTERNS`.

### `documento_empresa.pdf`

Arquivo PDF de exemplo. Deve ser usado com `PdfReader`, mas a rota HTTP atual nao usa esse leitor.

### `documento_empresa.odt`

Arquivo ODT de exemplo. Deve ser usado com `OdtReader`, mas a rota HTTP atual nao usa esse leitor.

## Banco JSON

`infrastructure/db/db.json` armazena:

```json
{
  "documents": []
}
```

## Log

`infrastructure/logs/logs.log` e o destino configurado para logs.

## Relacao com fluxo

Os dados de exemplo se relacionam com:

- [[fluxo/fluxo-http-atual]];
- [[Fluxo caso de Uso]];
- [[dependencias/dependencias]].

