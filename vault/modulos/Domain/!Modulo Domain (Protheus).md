O módulo **`domain`** é responsável por representar o **núcleo da regra de negócio** da aplicação. É nessa camada que ficam os conceitos do domínio, como entidades, modelos, enums e regras que descrevem o funcionamento do sistema, sem depender de frameworks ou tecnologias externas.

Normalmente, esse módulo contém:
- **Entidades (Entities)**
    - Representam os principais objetos do domínio e seus comportamentos.
- **Modelos de domínio**
    - Classes que descrevem os dados e conceitos fundamentais da aplicação.
- **Enums**
    - Tipos enumerados utilizados pelas regras de negócio, como tipos de documentos e extensões de arquivos.
- **Objetos de Valor (Value Objects)**
    - Objetos imutáveis que representam conceitos do domínio sem identidade própria.
- **Interfaces (quando pertencem ao domínio)**
    - Contratos relacionados às regras de negócio, independentes da implementação.