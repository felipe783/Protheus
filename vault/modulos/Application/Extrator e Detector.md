# Sobre os Arquivos

# Document Extractor

Responsabilidade:
- Esse arquivo implementa uma classe responsável por **extrair informações de um documento utilizando [Regex](https://regexr.com/).**
# Funcionalidades:

## Criação da Class e Def Extract

Primeiro é definida a classe `DocumentExtractor`, e o método `extract` é marcado como `@staticmethod`, permitindo que seja chamado sem instanciar a classe.
- O método recebe `content` (texto extraído do documento) e `document_type`, definido pelo [[Extrator e Detector#Document Detector|DocumentTypeDetector]]. O retorno é um `dict`.
- Os [[Patterns (Protheus)|Patterns]] são carregados conforme o tipo do documento. Se não houver padrões, retorna um `dict` vazio.
- O conteúdo é pré-processado: em geral é convertido para maiúsculas para facilitar o uso de regex, exceto no caso de arquivos `.xml` (como NF-e/DANFE), que mantêm a formatação original por serem sensíveis a isso.

````python
class DocumentExtractor:
    @staticmethod
    def extract(content: str, document_type: documentType) -> dict:
        patterns = DOCUMENT_PATTERNS.get(document_type)
        if not patterns:
            return {}
        if document_type != documentType.DANFE_XML: #NFE Pq ela é especial(.xml)
            content = content.upper()
````

## Criando o Resultado do Regex

Primeiro são definidas as `flags` do [Regex](https://regexr.com/), permitindo `.` incluir quebras de linha (`re.DOTALL`) e `^`/`$` funcionarem por linha (`re.MULTILINE`).
- Depois, para cada [[Patterns (Protheus)|Pattern]], é buscada a primeira ocorrência no texto e retornado o primeiro grupo capturado do [Regex](https://regexr.com/).
- Em seguida, o valor é limpo (remoção de ruídos/caracteres indesejados) e salvo em um `dict`, que será retornado no final.
````python
        flags = re.DOTALL | re.MULTILINE

        for field, pattern in patterns.items():
            match = re.search(pattern, content, flags)
            value = re.sub(r"\s+", " ", match.group(1)).strip() if match else None
            result[field] = value

        return result
````
# Document Detector

Responsabilidade:
 - Identificar automaticamente o tipo de documento com base no conteúdo do arquivo e sua extensão.
# Funcionalidades:

## Class e o Método "Detect" 

Primeiro o método é definido como `@staticmethod`,ele recebe os parâmetros `content` e `extension`, e retorna um `documentType`.
- Em seguida, o `content` é convertido para `lower case`, padronizando o texto
- Depois disso, é feita uma primeira filtragem específica para arquivos `.xml`, já que esse tipo de documento possui uma estrutura diferente dos demais formatos.

````python
class DocumentTypeDetector:
    @staticmethod
    def detect(
        content: str,
        extension: documentExtension
    ) -> documentType:
        content = content.lower()

        if extension == documentExtension.XML:
            if "<nfe" in content:
                return documentType.DANFE_XML
            if "<infnfe" in content:
                return documentType.DANFE_XML
            return documentType.DESCONHECIDO
````

## Classificação por palavras

Primeiro, o `scores` é inicializado como vazio. Em seguida, é iniciado um loop que conta quantas vezes as palavras do texto aparecem nas [[KeyWords (Protheus)|KeyWords]] de cada tipo.
- Para cada correspondência, é calculada uma pontuação e armazenada em `scores`.
- Ao final, o algoritmo seleciona o tipo com a maior pontuação, retornando o resultado mais provável.

````python
		scores = {}
        for doc_type, keywords in KEY_WORDS.items():
            score = 0
            for keyword in keywords:
                if keyword.lower() in content:
                    score += 1
            scores[doc_type] = score

        best_match = max(scores,key=scores.get)
        if scores[best_match] < 3:
            return documentType.DESCONHECIDO

        return best_match
````