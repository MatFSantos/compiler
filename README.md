# Lexical Analyzer and Syntactical Analyzer

O presente projeto se refere a um **analisador léxico e sintático**. O analisador léxico é capaz de definir os tokens e os possíveis erros de uma liguagem previamente já definida, já o analisador sintático, é capaz de verificar a lista de tokens que foi gerada a partir do léxico e capturar, se existir, qualquer tipo de erro sintático de acordo com a gramática já definida e baseada também nos tokens da linguagem. A linguagem conta com as seguintes regras léxicas:

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

Para executar o **analisador léxico** basta executar o comando `python run.py -l` na raíz do projeto ( dentro da pasta `lexical-analyzer`). É necessário fornecer os arquivos `.txt` contendo os textos que serão analisados na pasta `files/`.

Para executar o **analisador sintático** basta executar o comando `python run.py -sy` na raíz do projeto ( dentro da pasta `lexical-analyzer`). É necessário fornecer os arquivos `.txt` contendo os textos que serão analisados na pasta `files/`.
Todo o processo é feito no arquivo `run.py`, integrando todos os módulos.

Para executar ambos os analisadores, basta fornecer as duas flags *flags* ou simplesmente omití-las.

Vale ressaltar que ao fim da execução, os arquivos gerados terão os nomes originais concatenados com `[analisador usado]-saida.txt`. Todavia, sintático substitui, caso o arquivo apresente, o nome `lexico-saida.txt` por `sintatico-saida.txt`.

É possível também fornecer apenas um arquivo, passando o parâmetro `--name` no comando e fornecendo o nome do arquivo.

Fique atento: o arquivo ainda necessita está na pasta `/files`.

Esse modo de execução exige que seja escolhido ou o léxico ou sintático para a execução, pois os formatos de arquivos que são processados em ambos analisadores são diferentes.


## Testes
Foram feitos uma bateria de testes no módulo do analisador  léxico para verificar se tudo está correndo como o esperado e os tokens estão sendo gerados corretamente.

Os testes se encontram na pasta `tests/` e podem ser executados com o comando `python run.test.py` na raíz do projeto.

Para o analisador sintático, os testes foram simples e voltados apenas a escrita de código.

Os arquivos de teste para o analisador sintático estão na pasta `files-syntactical`

**OBS:** o comando `python` depende de como está instalado em sua máquina. A depender, pode ser `python3`
