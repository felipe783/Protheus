O Modulo **`core`** em um projeto deve conter tudo aquilo que é compartilhado por toda a aplicação e que ``não pertence a uma regra de negócio específica``. Ela concentra configurações, constantes, utilitários e componentes reutilizáveis que servem de base para o funcionamento do sistema.

Normalmente, a pasta `core` contém:
- **Configurações da aplicação**
    - Leitura de variáveis de ambiente.
    - Configuração de banco de dados, API Keys, URLs, etc.
- **Constantes**
    - Valores fixos utilizados em diversos módulos.
    - Exemplo: listas de palavras-chave, mensagens padrão, códigos de erro.
- **Enums**
    - Tipos enumerados compartilhados por todo o sistema.
- **Exceções customizadas**
    - Classes de erro específicas da aplicação.
- **Utilitários (Helpers)**
    - Funções genéricas reutilizáveis que não pertencem a um domínio específico.
- **Configuração de Logging**
    - Formatação e criação de logs da aplicação.
- **Segurança**
    - Funções de autenticação, geração de JWT, hash de senhas e permissões (quando aplicável).
- **Middlewares**
    - Componentes executados em todas as requisições, como CORS, logs, autenticação e tratamento de erros.
- **Dependências globais**
    - Dependências compartilhadas entre várias rotas utilizando o sistema de Dependency Injection do FastAPI.