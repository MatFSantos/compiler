# Lexical Analyzer

O presente projeto se refere a um **analisador léxico** capaz de definir os tokens e os possíveis erros de uma liguagem previamente já definida. A linguagem conta com as seguintes regras léxicas:

| Tokens                           | Formato                 |
|:--------------------------------:|:-----------------------:|
| *Palavras Reservadas*          | **variables, const, class, methods objects, main, return, if, else, then,for, read, print, void, int, real,boolean, string, true, false**    |
| *Identificadores*              | **letra (letra \| digito \| _)***   |
| *Números*                      | **digito+(.digito(digito)*)?**    |
| *Dígito*                       | **[0-9]**    |
| *Letra*                        | **[a-z] \| [A-Z]**    |
| *Operadores Aritméticos*       | **+ - * / ++ --**    |
| *Operadores Relacionais*       | **!= == < <= > >= =**    |
| *Operadores lógicos*           | **! && \|\|**    |
| *Comentários*                  | **// isto é um comentário de linha**|
| *Comentários*                  | **/ * isto é um comentário de bloco * /**|
| *Delimitadores*                | **; , . ( ) [ ] { } ->**    |
| *Cadeia de Caracteres*         | **"( letra \| digito \| símbolo )*"**    |
| *Símbolo*                      | **ASCII de 32 a 126 (exceto ASCII 34)**    |

## Dependências
O projeto não possui dependências para ser executado, porém foi utilizado para criar um ambiente de desenvolvimento um pacote do python chamado ***pipenv***. Não é necessário para executá-lo, porém caso deseje, veja o processo para ativar o ambiente de desenvolvimento [clicando aqui](https://willemallan.com.br/aprendendo-a-utilizar-o-pipenv/).

As dependências também podem ser vistas no arquivo `Pipfile`, que está vazio por o projeto não ter dependências.

A versão do python utilizada está listada no arquivo ```.python-version```

## Execução

Para executar o **analisador léxico** basta executar o comando `python run.py` na raíz do projeto ( dentro da pasta `lexical-analyzer`). É necessário fornecer os arquivos `.txt` contendo os textos que serão analisados na pasta `files/`.

Todo o processo é feito no arquivo `run.py`, integrando todos os módulos.

## Testes
Foram feitos uma bateria de testes no módulo do analisador para verificar se tudo está correndo como o esperado e os tokens estão sendo gerados corretamente.

Os testes se encontram na pasta `tests/` e podem ser executados com o comando `python run.test.py` na raíz do projeto.

**OBS:** o comando `python` depende de como está instalado em sua máquina. A depender, pode ser `python3`
