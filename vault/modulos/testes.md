# Modulo Testes

Os testes ficam em `test/` e usam `pytest`.

## `test/test_db.py`

Testa:

- retorno padrao quando o banco nao existe;
- salvar e carregar dados;
- retorno padrao quando o JSON esta corrompido.

Observacao tecnica: o teste altera `core.dbPathConfig.DB_PATH`, mas a implementacao real em `JsonRepositoryDeps.py` usa um `DB_PATH` definido localmente. Isso pode impedir o isolamento esperado.

## `test/test_log.py`

Testa se `save_db` gera log.

Observacao tecnica: o teste espera a string `"Salvo com sucesso"`, mas a implementacao registra `"DB salvo com sucesso..."`. Isso pode causar falha dependendo do texto capturado.

## Comando

```powershell
python -m pytest -v
```

## Relacao com o sistema

Os testes cobrem principalmente [[modulos/infrastructure]], nao o fluxo HTTP de [[modulos/api]] nem os detectores de [[modulos/application]].

