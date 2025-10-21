# TermIA - Especificação de Comandos e Gramática

## 1. Visão Geral

Este documento especifica todos os comandos implementados no TermIA (Terminal Inteligente), incluindo comandos do sistema operacional, comandos de IA e comandos de controle do terminal.

---

## 2. Comandos do Sistema Operacional

### 2.1 `ls` - Listar arquivos e diretórios

**Sintaxe:**
```
ls [opções] [caminho]
```

**Descrição:** Lista o conteúdo de um diretório.

**Opções:**
- `-a` : Mostra arquivos ocultos
- `-l` : Formato detalhado (long format)
- `-h` : Tamanhos legíveis (human-readable)

**Exemplos:**
```
ls
ls -a
ls -l /home/usuario
ls -lah .
```

---

### 2.2 `cd` - Mudar diretório

**Sintaxe:**
```
cd [caminho]
```

**Descrição:** Altera o diretório de trabalho atual.

**Exemplos:**
```
cd /home/usuario
cd ..
cd ~/documentos
cd
```

**Comportamento especial:**
- `cd` sem argumentos vai para o diretório home
- `cd -` volta para o diretório anterior

---

### 2.3 `mkdir` - Criar diretório

**Sintaxe:**
```
mkdir [opções] <nome_diretorio>
```

**Descrição:** Cria um ou mais diretórios.

**Opções:**
- `-p` : Cria diretórios pais se necessário

**Exemplos:**
```
mkdir novo_projeto
mkdir -p projetos/2024/termia
```

---

### 2.4 `pwd` - Mostrar diretório atual

**Sintaxe:**
```
pwd
```

**Descrição:** Exibe o caminho completo do diretório de trabalho atual.

**Exemplo:**
```
pwd
# Saída: /home/usuario/projetos
```

---

### 2.5 `cat` - Exibir conteúdo de arquivo

**Sintaxe:**
```
cat <arquivo>
```

**Descrição:** Mostra o conteúdo de um arquivo de texto.

**Exemplo:**
```
cat readme.txt
cat arquivo.py
```

---

## 3. Comandos de Inteligência Artificial

Todos os comandos de IA utilizam o prefixo `ia` seguido do subcomando.

### 3.1 `ia ask` - Perguntas gerais

**Sintaxe:**
```
ia ask "<pergunta>"
```

**Descrição:** Faz uma pergunta geral à IA e recebe uma resposta.

**Exemplos:**
```
ia ask "Qual é a capital da França?"
ia ask "Como funciona recursão?"
ia ask "Explique o que é um compilador"
```

---

### 3.2 `ia summarize` - Resumir texto

**Sintaxe:**
```
ia summarize "<texto>" [--length short|medium|long]
```

**Descrição:** Gera um resumo do texto fornecido.

**Opções:**
- `--length short` : Resumo curto (padrão)
- `--length medium` : Resumo médio
- `--length long` : Resumo detalhado

**Exemplos:**
```
ia summarize "Lorem ipsum dolor sit amet..."
ia summarize "$(cat artigo.txt)" --length medium
```

---

### 3.3 `ia codeexplain` - Explicar código

**Sintaxe:**
```
ia codeexplain <arquivo>
```

**Descrição:** Analisa e explica o código contido no arquivo especificado.

**Exemplos:**
```
ia codeexplain main.py
ia codeexplain lexer.c
```

---

### 3.4 `ia translate` - Traduzir texto

**Sintaxe:**
```
ia translate "<texto>" --to <idioma>
```

**Descrição:** Traduz o texto fornecido para o idioma especificado.

**Idiomas suportados:** pt, en, es, fr, de, it

**Exemplos:**
```
ia translate "Hello World" --to pt
ia translate "Como você está?" --to en
```

---

## 4. Comandos de Controle do Terminal

### 4.1 `history` - Histórico de comandos

**Sintaxe:**
```
history [n]
```

**Descrição:** Exibe o histórico dos últimos comandos executados.

**Parâmetros:**
- `n` : Número de comandos a exibir (padrão: 10)

**Exemplos:**
```
history
history 20
```

---

### 4.2 `clear` - Limpar tela

**Sintaxe:**
```
clear
```

**Descrição:** Limpa a tela do terminal.

---

### 4.3 `help` - Ajuda

**Sintaxe:**
```
help [comando]
```

**Descrição:** Exibe informações de ajuda sobre comandos disponíveis.

**Exemplos:**
```
help
help ls
help ia
```

---

### 4.4 `exit` - Sair do terminal

**Sintaxe:**
```
exit
```

**Descrição:** Encerra a sessão do TermIA.

---

## 5. Gramática Formal

### 5.1 Definição em BNF

```bnf
<command>           ::= <os_command> | <ia_command> | <control_command>

<os_command>        ::= <ls_cmd> | <cd_cmd> | <mkdir_cmd> | <pwd_cmd> | <cat_cmd>

<ls_cmd>            ::= "ls" [<ls_options>] [<path>]
<ls_options>        ::= "-" <ls_flags>
<ls_flags>          ::= "a" | "l" | "h" | "al" | "ah" | "lh" | "alh"

<cd_cmd>            ::= "cd" [<path>]

<mkdir_cmd>         ::= "mkdir" ["-p"] <path>

<pwd_cmd>           ::= "pwd"

<cat_cmd>           ::= "cat" <path>

<ia_command>        ::= "ia" <ia_subcommand>
<ia_subcommand>     ::= <ia_ask> | <ia_summarize> | <ia_codeexplain> | <ia_translate>

<ia_ask>            ::= "ask" <quoted_string>

<ia_summarize>      ::= "summarize" <quoted_string> [<length_option>]
<length_option>     ::= "--length" ("short" | "medium" | "long")

<ia_codeexplain>    ::= "codeexplain" <path>

<ia_translate>      ::= "translate" <quoted_string> "--to" <language>
<language>          ::= "pt" | "en" | "es" | "fr" | "de" | "it"

<control_command>   ::= <history_cmd> | <clear_cmd> | <help_cmd> | <exit_cmd>

<history_cmd>       ::= "history" [<number>]

<clear_cmd>         ::= "clear"

<help_cmd>          ::= "help" [<command_name>]

<exit_cmd>          ::= "exit"

<path>              ::= <identifier> | <path> "/" <identifier> | "." | ".." | "~"

<quoted_string>     ::= '"' <string_content> '"'

<string_content>    ::= <any_char>*

<command_name>      ::= <identifier>

<number>            ::= <digit>+

<identifier>        ::= <letter> (<letter> | <digit> | "_" | "-" | ".")*

<letter>            ::= "a" | "b" | ... | "z" | "A" | "B" | ... | "Z"

<digit>             ::= "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9"
```

---

## 6. Tokens Léxicos

### 6.1 Palavras-chave (Keywords)
```
LS, CD, MKDIR, PWD, CAT
IA, ASK, SUMMARIZE, CODEEXPLAIN, TRANSLATE
HISTORY, CLEAR, HELP, EXIT
```

### 6.2 Operadores e Símbolos
```
DASH         : "-"
SLASH        : "/"
DOT          : "."
TILDE        : "~"
QUOTE        : '"'
```

### 6.3 Literais
```
STRING       : sequência de caracteres entre aspas
NUMBER       : sequência de dígitos
IDENTIFIER   : nome de arquivo, diretório ou comando
PATH         : caminho de arquivo/diretório
```

### 6.4 Opções
```
OPTION_FLAG  : "-" seguido de letras (ex: -a, -l, -p)
LONG_OPTION  : "--" seguido de palavra (ex: --length, --to)
```

---

## 7. Tratamento de Erros

### 7.1 Mensagens de Erro Padrão

| Código | Mensagem | Descrição |
|--------|----------|-----------|
| ERR_001 | `Comando não encontrado: <comando>` | Comando não existe no TermIA |
| ERR_002 | `Sintaxe inválida` | Erro de sintaxe no comando |
| ERR_003 | `Arquivo não encontrado: <arquivo>` | Arquivo especificado não existe |
| ERR_004 | `Permissão negada` | Sem permissão para executar operação |
| ERR_005 | `Diretório não encontrado: <diretório>` | Diretório especificado não existe |
| ERR_006 | `Opção inválida: <opção>` | Opção não suportada |
| ERR_007 | `Argumento obrigatório ausente` | Falta argumento necessário |
| ERR_008 | `Falha na conexão com API de IA` | Erro ao conectar com serviço de IA |

### 7.2 Tratamento de Aspas

- Strings devem ser delimitadas por aspas duplas `"`
- Aspas não fechadas geram erro de sintaxe
- Suporte a escape de aspas: `\"` dentro de strings

---

## 8. Recursos Extras Implementados

### 8.1 Histórico Persistente
- Armazena últimos 100 comandos
- Salvos em arquivo `.termia_history`
- Navegação com setas (↑↓)

### 8.2 Autocompletar
- Tab para autocompletar comandos
- Tab para autocompletar caminhos de arquivos
- Sugestões inteligentes baseadas no contexto

### 8.3 Mensagens de Ajuda Contextuais
- `help` sem argumentos lista todos comandos
- `help <comando>` mostra ajuda específica
- Sugestões de comandos similares quando há erro

### 8.4 Modo Verboso
- Opção `--verbose` para debug
- Mostra tokens reconhecidos
- Exibe árvore sintática

---

## 9. Exemplos de Sessão Completa

```bash
TermIA v1.0 - Terminal Inteligente
Digite 'help' para ajuda ou 'exit' para sair

~/projetos$ ls -la
drwxr-xr-x  3 user user 4096 Out 16 10:30 .
drwxr-xr-x 10 user user 4096 Out 15 14:20 ..
-rw-r--r--  1 user user  256 Out 16 10:30 main.py

~/projetos$ mkdir novo_projeto

~/projetos$ cd novo_projeto

~/projetos/novo_projeto$ ia ask "O que é um lexer?"
Um lexer (ou analisador léxico) é a primeira fase de um compilador. 
Ele lê o código fonte e o divide em tokens, que são as unidades 
básicas de significado, como palavras-chave, identificadores, 
operadores e literais.

~/projetos/novo_projeto$ cat ../main.py
def main():
    print("Hello TermIA")

~/projetos/novo_projeto$ ia codeexplain ../main.py
Este código Python define uma função main() que imprime a mensagem 
"Hello TermIA" no console. É um exemplo simples de função em Python.

~/projetos/novo_projeto$ history 5
1. ls -la
2. mkdir novo_projeto
3. cd novo_projeto
4. ia ask "O que é um lexer?"
5. cat ../main.py

~/projetos/novo_projeto$ exit
Até logo!
```

---

## 10. Arquitetura de Implementação

### 10.1 Módulos Principais

```
termia/
├── lexer.py          # Analisador léxico
├── parser.py         # Analisador sintático
├── executor.py       # Executor de comandos
├── ia_integration.py # Integração com API de IA
├── history.py        # Gerenciamento de histórico
├── autocomplete.py   # Sistema de autocompletar
├── main.py           # Loop principal do terminal
└── utils.py          # Funções auxiliares
```

### 10.2 Fluxo de Execução

1. **Input** → Usuário digita comando
2. **Lexer** → Tokenização do comando
3. **Parser** → Análise sintática e criação da AST
4. **Validator** → Validação semântica
5. **Executor** → Execução do comando
6. **Output** → Exibição do resultado

---

## 11. Próximos Passos

### Semana 1-3 (Entrega Parcial)
- [x] Definir gramática completa
- [ ] Implementar lexer para todos os tokens
- [ ] Implementar parser básico
- [ ] Testes unitários do lexer/parser

### Semana 4-8 (Entrega Final)
- [ ] Implementar executor de comandos SO
- [ ] Integrar API de IA
- [ ] Implementar histórico e autocomplete
- [ ] Testes de integração
- [ ] Documentação completa
- [ ] Apresentação

---

**Versão:** 1.0  
**Data:** Outubro 2024  
**Autor:** [Seu Nome]  
**Disciplina:** ECOI26 - Compiladores  
**Professor:** Walter Aoiama Nagai