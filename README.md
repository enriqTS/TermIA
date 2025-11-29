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

## Testes

### Estrutura de Testes

```
tests/
├── test_lexer.py          # Testes do analisador léxico
├── test_parser.py         # Testes do analisador sintático
├── test_executor.py       # Testes do executor
├── test_ia_commands.py    # Testes dos comandos IA
└── fixtures/              # Arquivos de teste
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