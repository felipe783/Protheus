# Sobre o Arquivo

Este arquivo configura o módulo `logging` do Python, definindo **como e onde as mensagens de log serão gravadas**. Após essa configuração, qualquer chamada como `logging.info()`, `logging.warning()` ou `logging.error()` seguirá essas regras.

````python
logging.basicConfig(
    filename="infrastructure/logs/uploads_logs.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8"
)
````

Hierarquia dos Níveis 

| Nível      | Uso                                                        |
| ---------- | ---------------------------------------------------------- |
| `DEBUG`    | Informações detalhadas para depuração.                     |
| `INFO`     | Eventos normais da aplicação.                              |
| `WARNING`  | Situações inesperadas, mas que não interrompem o programa. |
| `ERROR`    | Erros que impedem uma operação de ser concluída.           |
| `CRITICAL` | Erros muito graves que podem interromper a aplicação.      |
