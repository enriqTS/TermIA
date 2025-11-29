# TermIA - Terminal Inteligente 🚀

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![PLY](https://img.shields.io/badge/PLY-3.11-green.svg)](https://www.dabeaz.com/ply/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**TermIA** é um terminal inteligente desenvolvido como projeto final da disciplina de Compiladores (ECOI26) da Universidade Federal de Itajubá. O projeto integra conceitos de análise léxica, análise sintática e inteligência artificial para criar um shell personalizado.

## Índice

- [Características](#-características)
- [Instalação](#-instalação)
- [Uso](#-uso)
- [Comandos Disponíveis](#-comandos-disponíveis)
- [Arquitetura](#-arquitetura)
- [Gramática da Linguagem](#-gramática-da-linguagem)
- [Testes](#-testes)
- [Licença](#-licença)

## Características

### Comandos do Sistema Operacional
- `ls` - Listar arquivos e diretórios (com opções -a, -l, -h)
- `cd` - Navegar entre diretórios
- `mkdir` - Criar diretórios (com opção -p)
- `pwd` - Mostrar diretório atual
- `cat` - Exibir conteúdo de arquivos

### Comandos de Inteligência Artificial
- `ia ask` - Fazer perguntas gerais
- `ia summarize` - Resumir textos
- `ia codeexplain` - Explicar código
- `ia translate` - Traduzir textos

### Recursos Extras
- **Histórico de comandos** persistente
- **Autocomplete** inteligente
- **Syntax highlighting**
- **Mensagens de erro claras**
- **Modo seguro** para comandos perigosos

## Instalação

### Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)
- Git

### Passos de Instalação

1. **Clone o repositório:**
```bash
git clone https://github.com/enriqTS/TermIA.git
cd TermIA
```

2. **Crie um ambiente virtual:**
```bash
python3 -m venv venv
source venv/bin/activate  # No Linux/Mac
# ou
venv\Scripts\activate  # No Windows
```

3. **Instale as dependências:**
```bash
pip install ply pytest colorama requests pyyaml prompt_toolkit pygments
```

4. **Execute o TermIA:**
```bash
python main.py
# ou 
python3 main.py
```

## Uso

### Iniciar o Terminal

```bash
python main.py
```

### Exemplos de Comandos

#### Comandos do Sistema
```bash
TermIA> ls -la
TermIA> cd ~
TermIA> mkdir -p new_project/src
TermIA> pwd
TermIA> cat README.md
```

#### Comandos de IA
```bash
TermIA> ia ask "O que é um compilador?"
TermIA> ia summarize "Texto" --length medium
TermIA> ia codeexplain main.py
TermIA> ia translate "Hello World" --to pt
```

#### Comandos de Controle
```bash
TermIA> history 20
TermIA> help ls
TermIA> clear
TermIA> exit
```

## Comandos Disponíveis

### Sistema Operacional

| Comando | Descrição | Exemplos |
|---------|-----------|----------|
| `ls [opções] [path]` | Lista arquivos e diretórios | `ls -la`, `ls /home` |
| `cd [path]` | Muda de diretório | `cd ..`, `cd ~` |
| `mkdir [-p] <dir>` | Cria diretório | `mkdir test`, `mkdir -p a/b/c` |
| `pwd` | Mostra diretório atual | `pwd` |
| `cat <file>` | Exibe conteúdo de arquivo | `cat file.txt` |

### Inteligência Artificial

| Comando | Descrição | Exemplos |
|---------|-----------|----------|
| `ia ask "<question>"` | Faz pergunta à IA | `ia ask "O que é Python?"` |
| `ia summarize "<text>"` | Resume texto | `ia summarize "..." --length short` |
| `ia codeexplain <file>` | Explica código | `ia codeexplain script.py` |
| `ia translate "<text>" --to <lang>` | Traduz texto | `ia translate "Hi" --to pt` |

### Controle

| Comando | Descrição | Exemplos |
|---------|-----------|----------|
| `history [n]` | Mostra histórico | `history`, `history 10` |
| `clear` | Limpa a tela | `clear` |
| `help [cmd]` | Exibe ajuda | `help`, `help ls` |
| `exit` | Sai do terminal | `exit` |

## Arquitetura

### Componentes Principais

```
┌─────────────┐
│   Input     │  ← Comando do usuário
└──────┬──────┘
       │
┌──────▼──────┐
│    Lexer    │  ← Análise léxica (tokens)
└──────┬──────┘
       │
┌──────▼──────┐
│   Parser    │  ← Análise sintática (AST)
└──────┬──────┘
       │
┌──────▼──────┐
│  Executor   │  ← Execução do comando
└──────┬──────┘
       │
┌──────▼──────┐
│   Output    │  ← Resultado para o usuário
└─────────────┘
```


## Gramática da Linguagem

### Visão Geral

Esta seção especifica todos os comandos implementados no TermIA (Terminal Inteligente), incluindo comandos do sistema operacional, comandos de IA e comandos de controle do terminal. Ela descreve tanto a sintaxe informal (como o usuário digita) quanto a gramática formal em BNF e os tokens léxicos reconhecidos pelo analisador.

---

### Comandos do Sistema Operacional

#### `ls` - Listar arquivos e diretórios

**Sintaxe:**
```bash
ls [opções] [caminho]
```

**Descrição:** Lista o conteúdo de um diretório.

**Opções:**
- `-a` : Mostra arquivos ocultos
- `-l` : Formato detalhado (*long format*)
- `-h` : Tamanhos legíveis (*human-readable*)

**Exemplos:**
```bash
ls
ls -a
ls -l /home/usuario
ls -lah .
```

---

#### `cd` - Mudar diretório

**Sintaxe:**
```bash
cd [caminho]
```

**Descrição:** Altera o diretório de trabalho atual.

**Exemplos:**
```bash
cd /home/usuario
cd ..
cd ~/documentos
cd
```

---

#### `mkdir` - Criar diretório

**Sintaxe:**
```bash
mkdir [opções] <nome_diretorio>
```

**Descrição:** Cria um ou mais diretórios.

**Opções:**
- `-p` : Cria diretórios pais se necessário

**Exemplos:**
```bash
mkdir novo_projeto
mkdir -p projetos/2024/termia
```

---

#### `pwd` - Mostrar diretório atual

**Sintaxe:**
```bash
pwd
```

**Descrição:** Exibe o caminho completo do diretório de trabalho atual.

**Exemplo:**
```bash
pwd
# Saída: /home/usuario/projetos
```

---

#### `cat` - Exibir conteúdo de arquivo

**Sintaxe:**
```bash
cat <arquivo>
```

**Descrição:** Mostra o conteúdo de um arquivo de texto.

**Exemplos:**
```bash
cat readme.txt
cat arquivo.py
```

---

### Comandos de Inteligência Artificial

Todos os comandos de IA utilizam o prefixo `ia` seguido do subcomando.

#### `ia ask` - Perguntas gerais

**Sintaxe:**
```bash
ia ask "<pergunta>"
```

**Descrição:** Faz uma pergunta geral à IA e recebe uma resposta.

**Exemplos:**
```bash
ia ask "Qual é a capital da França?"
ia ask "Como funciona recursão?"
ia ask "Explique o que é um compilador"
```

---

#### `ia summarize` - Resumir texto

**Sintaxe:**
```bash
ia summarize "<texto>" [--length short|medium|long]
```

**Descrição:** Gera um resumo do texto fornecido.

**Opções:**
- `--length short`  : Resumo curto (padrão)
- `--length medium` : Resumo médio
- `--length long`   : Resumo detalhado

**Exemplos:**
```bash
ia summarize "Lorem ipsum dolor sit amet..."
ia summarize "$(cat artigo.txt)" --length medium
```

---

#### `ia codeexplain` - Explicar código

**Sintaxe:**
```bash
ia codeexplain <arquivo>
```

**Descrição:** Analisa e explica o código contido no arquivo especificado.

**Exemplos:**
```bash
ia codeexplain main.py
ia codeexplain lexer.c
```

---

#### `ia translate` - Traduzir texto

**Sintaxe:**
```bash
ia translate "<texto>" --to <idioma>
```

**Descrição:** Traduz o texto fornecido para o idioma especificado.

**Idiomas típicos:** `pt`, `en`, `es`, `fr`, `de`, `it`

**Exemplos:**
```bash
ia translate "Hello World" --to pt
ia translate "Como você está?" --to en
```

---

### Comandos de Controle do Terminal

#### `history` - Histórico de comandos

**Sintaxe:**
```bash
history [n]
```

**Descrição:** Exibe o histórico dos últimos comandos executados.

**Parâmetros:**
- `n` : Número de comandos a exibir (padrão: 10)

**Exemplos:**
```bash
history
history 20
```

---

#### `clear` - Limpar tela

**Sintaxe:**
```bash
clear
```

**Descrição:** Limpa a tela do terminal.

---

#### `help` - Ajuda

**Sintaxe:**
```bash
help [comando]
```

**Descrição:** Exibe informações de ajuda sobre comandos disponíveis.

**Exemplos:**
```bash
help
help ls
help ia
```

---

#### `exit` - Sair do terminal

**Sintaxe:**
```bash
exit
```

**Descrição:** Encerra a sessão do TermIA.

---

### Gramática Formal (BNF)

```bnf
<command>           ::= <os_command> | <ia_command> | <control_command>

<os_command>        ::= <ls_cmd> | <cd_cmd> | <mkdir_cmd> | <pwd_cmd> | <cat_cmd>

<ls_cmd>            ::= "ls" [<ls_options>] [<path>]
<ls_options>        ::= OPTION_SHORT      ; ex: -a, -l, -h, -la, -lah

<cd_cmd>            ::= "cd" [<path>]

<mkdir_cmd>         ::= "mkdir" ["-p"] <path>

<pwd_cmd>           ::= "pwd"

<cat_cmd>           ::= "cat" <path>

<ia_command>        ::= "ia" <ia_subcommand>
<ia_subcommand>     ::= <ia_ask> | <ia_summarize> | <ia_codeexplain> | <ia_translate>

<ia_ask>            ::= "ask" <quoted_string>

<ia_summarize>      ::= "summarize" <quoted_string> [<length_option>]
<length_option>     ::= "--length" <identifier>
  ; valores esperados: "short" | "medium" | "long"

<ia_codeexplain>    ::= "codeexplain" <path>

<ia_translate>      ::= "translate" <quoted_string> <translate_option>
<translate_option>  ::= "--to" <identifier>
  ; valores típicos: "pt" | "en" | "es" | "fr" | "de" | "it"

<control_command>   ::= <history_cmd> | <clear_cmd> | <help_cmd> | <exit_cmd>

<history_cmd>       ::= "history" [<number>]

<clear_cmd>         ::= "clear"

<help_cmd>          ::= "help" [<command_name>]

<exit_cmd>          ::= "exit"

<path>              ::= PATH | IDENTIFIER | "." | ".." | "~"

<quoted_string>     ::= '"' <string_content> '"'

<string_content>    ::= <any_char>*

<command_name>      ::= <identifier>

<number>            ::= <digit>+

<identifier>        ::= <letter> (<letter> | <digit> | "_" | "-" | ".")*

<letter>            ::= "a" | "b" | ... | "z" | "A" | "B" | ... | "Z"

<digit>             ::= "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9"
```

---

### Tokens Léxicos

#### Palavras-chave (*Keywords*)

```text
LS, CD, MKDIR, PWD, CAT
IA, ASK, SUMMARIZE, CODEEXPLAIN, TRANSLATE
HISTORY, CLEAR, HELP, EXIT
```

#### Operadores e Símbolos

```text
DOT          : "."
DOTDOT       : ".."
TILDE        : "~"
```

#### Literais

```text
STRING       : sequência de caracteres entre aspas
NUMBER       : sequência de dígitos
IDENTIFIER   : nome de arquivo, diretório ou comando
PATH         : caminho de arquivo/diretório
```

#### Opções

```text
OPTION_SHORT : "-" seguido de uma ou mais letras (ex: -a, -l, -p, -la, -lah)
LONG_OPTION  : "--" seguido de palavra (ex: --length, --to)
```


## Testes

### Estrutura de Testes

```
tests/
├── test_ai_api.py                 # Teste padrão da API fornecido pelo professor
├── test_lexer.py                  # Testes do analisador léxico
├── test_parser.py                 # Testes do analisador sintático
├── test_executor.py               # Testes do executor do SO
├── test_ia_commands.py            # Testes dos comandos IA
└── test_enhanced_features.py      # Testes de features adicionais pedidas
```

### Executar Testes Específicos

```bash
# Testar apenas o lexer
pytest tests/test_lexer.py -v

# Testar com output detalhado
pytest tests/ -vv

# Testar e parar no primeiro erro
pytest tests/ -x
```

## Autores

- **Henrique Teixeira Silva** - *Desenvolvimento* - [@enriqTS](https://github.com/enriqTS)
- **Argéu Venturini Souza Rodrigues** - *Desenvolvimento* - [@Argeu42](https://github.com/Argeu42)

## Informações Acadêmicas

- **Disciplina:** ECOI26 - Compiladores
- **Professor:** Walter Aoiama Nagai
- **Instituição:** Universidade Federal de Itajubá - Campus Itabira
- **Curso:** Engenharia de Computação

## Licença

Este projeto está sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## Agradecimentos

- Professor Walter Aoiama Nagai

---

**Desenvolvido para a disciplina de Compiladores - UNIFEI**