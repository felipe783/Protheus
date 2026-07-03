
O módulo **`infrastructure`** é responsável por lidar com todos os **detalhes técnicos e externos da aplicação**. É nessa camada que ficam as implementações concretas necessárias para conectar o sistema ao “mundo real”, como banco de dados, serviços externos, arquivos e bibliotecas específicas.

Normalmente, esse módulo contém:

- **Repositórios (implementações)**
    - Classes que implementam os contratos definidos no `domain` ou `application`, acessando o banco de dados.
- **Banco de dados**
    - Conexões, sessões, migrations e configuração do ORM (SQLAlchemy, Tortoise, etc).
- **Integrações externas**
    - Comunicação com APIs externas, serviços de terceiros, filas (RabbitMQ, Kafka), storage, etc.
- **File system**
    - Leitura e escrita de arquivos, upload/download, manipulação de diretórios.
- **Implementações técnicas de interfaces**
    - Qualquer classe que cumpre um contrato definido nas camadas superiores.
- **Adapters**
    - Tradução entre o formato do domínio e o formato externo (DTOs, schemas, respostas de APIs externas).