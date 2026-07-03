O módulo **`application`** é responsável por **orquestrar os casos de uso da aplicação**. É nessa camada que ficam os fluxos que coordenam as regras de negócio, chamando os componentes do domínio e da infraestrutura para executar uma funcionalidade completa.

Normalmente, esse módulo contém:
- **Use Cases**
    - Implementam as funcionalidades do sistema, coordenando todas as etapas necessárias para atender uma requisição.
- **Services (quando utilizados)**
    - Agrupam operações da aplicação que podem ser reutilizadas por diferentes casos de uso.
- **Interfaces (Ports)**
    - Definem contratos que serão implementados pela camada de infraestrutura, promovendo baixo acoplamento.
- **Orquestração do fluxo**
    - Coordena chamadas para repositórios, serviços externos e componentes do domínio, sem conhecer detalhes de implementação.