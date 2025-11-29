#!/usr/bin/env python3
"""
TermIA - Terminal Inteligente
Arquivo principal para executar o terminal.
"""

import sys
import os

# Garante que o diretório src está no path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, 'src')
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

# Imports do projeto
from parser import TermIAParser
from executor import CommandExecutor, SecurityException
from ai_executor import AIExecutor, AIException
from enhanced_input import EnhancedInputHandler
import ast_nodes

# Importa as classes AST explicitamente
LSCommand = ast_nodes.LSCommand
CDCommand = ast_nodes.CDCommand
MkdirCommand = ast_nodes.MkdirCommand
PwdCommand = ast_nodes.PwdCommand
CatCommand = ast_nodes.CatCommand
IAAskCommand = ast_nodes.IAAskCommand
IASummarizeCommand = ast_nodes.IASummarizeCommand
IACodeExplainCommand = ast_nodes.IACodeExplainCommand
IATranslateCommand = ast_nodes.IATranslateCommand
HistoryCommand = ast_nodes.HistoryCommand
ClearCommand = ast_nodes.ClearCommand
HelpCommand = ast_nodes.HelpCommand
ExitCommand = ast_nodes.ExitCommand

try:
    from colorama import init, Fore, Style
    init(autoreset=True)
    COLORS_AVAILABLE = True
except ImportError:
    COLORS_AVAILABLE = False
    # Fallback se colorama não estiver instalado
    class Fore:
        GREEN = ''
        YELLOW = ''
        RED = ''
        CYAN = ''
        MAGENTA = ''
        BLUE = ''
        RESET = ''
    
    class Style:
        BRIGHT = ''
        RESET_ALL = ''


class TermIA:
    "Classe principal do TermIA."
    
    def __init__(self, debug_mode=False, enhanced_mode=True):
        "Inicializa o TermIA."
        self.parser = TermIAParser()
        self.executor = CommandExecutor()
        self.ai_executor = AIExecutor()
        self.enhanced_mode = enhanced_mode

        # Initialize enhanced input if available
        if enhanced_mode:
            try:
                self.input_handler = EnhancedInputHandler('.termia_history')
                self.history = []  # History managed by input handler
            except Exception as e:
                print(f"{Fore.YELLOW}Warning: Enhanced mode failed, using basic input: {e}{Style.RESET_ALL}")
                self.enhanced_mode = False
                self.history = []
        else:
            self.history = []

        self.running = True
        self.current_dir = os.getcwd()
        self.debug_mode = debug_mode
    
    def print_banner(self):
        "Imprime a logo bonita do shell."
        banner = f"""
            {Fore.CYAN}{Style.BRIGHT}╔═══════════════════════════════════════════════════════╗
            ║                                                       ║
            ║   {Fore.MAGENTA}████████╗███████╗██████╗ ███╗   ███╗██╗ █████╗ {Fore.CYAN}     ║
            ║   {Fore.MAGENTA}╚══██╔══╝██╔════╝██╔══██╗████╗ ████║██║██╔══██╗{Fore.CYAN}     ║
            ║   {Fore.MAGENTA}   ██║   █████╗  ██████╔╝██╔████╔██║██║███████║{Fore.CYAN}     ║
            ║   {Fore.MAGENTA}   ██║   ██╔══╝  ██╔══██╗██║╚██╔╝██║██║██╔══██║{Fore.CYAN}     ║
            ║   {Fore.MAGENTA}   ██║   ███████╗██║  ██║██║ ╚═╝ ██║██║██║  ██║{Fore.CYAN}     ║
            ║   {Fore.MAGENTA}   ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝╚═╝  ╚═╝{Fore.CYAN}     ║
            ║                                                       ║
            ║         {Fore.YELLOW}Terminal Inteligente - Versão 2.0{Fore.CYAN}             ║
            ║         {Fore.GREEN}Projeto de Compiladores - UNIFEI{Fore.CYAN}              ║
            ║            {Fore.GREEN}Autores: Argéu e Henrique{Fore.CYAN}                  ║
            ║                                                       ║
            ╚═══════════════════════════════════════════════════════╝{Style.RESET_ALL}

            {Fore.YELLOW}Digite 'help' para ajuda ou 'exit' para sair{Style.RESET_ALL}
            """
        print(banner)
    
    def get_prompt(self):
        "Retorna o prompt do terminal."
        # Mostra apenas o nome do diretório atual
        dir_name = os.path.basename(self.current_dir)
        if not dir_name:
            dir_name = self.current_dir

        # Use different prompt formatting for enhanced vs basic mode
        if self.enhanced_mode:
            # prompt_toolkit uses FormattedText with tuples
            from prompt_toolkit.formatted_text import FormattedText
            return FormattedText([
                ('#00ff00', dir_name),      # Green for directory
                ('#00ffff', ' TermIA> '),   # Cyan for prompt
            ])
        else:
            # Basic mode uses colorama
            return f"{Fore.GREEN}{dir_name}{Fore.CYAN} TermIA>{Style.RESET_ALL} "
    
    def _check_restricted_command(self, command: str) -> bool:
        """
        Verifica se o comando contém padrões restritos e exibe aviso.

        Args:
            command: String com o comando a ser verificado

        Returns:
            True se o comando está bloqueado, False caso contrário
        """
        # Lista de comandos perigosos conhecidos (além dos configurados)
        dangerous_patterns = [
            ('rm', 'remove/delete files'),
            ('format', 'format disk'),
            ('mkfs', 'create filesystem'),
            ('dd', 'disk dump/write'),
            ('fdisk', 'partition disk'),
            ('parted', 'partition editor'),
            ('mkswap', 'create swap'),
            ('reboot', 'reboot system'),
            ('shutdown', 'shutdown system'),
            ('halt', 'halt system'),
            ('poweroff', 'power off system'),
            ('kill -9', 'force kill process'),
        ]

        command_lower = command.lower()

        # Verifica padrões conhecidos
        for pattern, description in dangerous_patterns:
            if pattern in command_lower:
                print(f"\n{Fore.RED}{'=' * 70}{Style.RESET_ALL}")
                print(f"{Fore.RED}{Style.BRIGHT}⚠  COMANDO BLOQUEADO POR SEGURANÇA{Style.RESET_ALL}")
                print(f"{Fore.RED}{'=' * 70}{Style.RESET_ALL}\n")
                print(f"{Fore.YELLOW}Comando detectado:{Style.RESET_ALL} {Fore.RED}{pattern}{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}Descrição:{Style.RESET_ALL} {description}")
                print(f"\n{Fore.CYAN}ℹ  TermIA bloqueia comandos destrutivos para sua segurança.{Style.RESET_ALL}")
                print(f"{Fore.CYAN}   Este é um terminal educacional focado em compiladores.{Style.RESET_ALL}\n")
                print(f"{Fore.GREEN}Comandos disponíveis:{Style.RESET_ALL}")
                print(f"  • OS: {Fore.CYAN}ls, cd, mkdir, pwd, cat{Style.RESET_ALL}")
                print(f"  • IA: {Fore.CYAN}ia ask, ia summarize, ia codeexplain, ia translate{Style.RESET_ALL}")
                print(f"  • Controle: {Fore.CYAN}history, clear, help, exit{Style.RESET_ALL}")
                print(f"\n{Fore.YELLOW}Use 'help' para mais informações{Style.RESET_ALL}\n")
                print(f"{Fore.RED}{'=' * 70}{Style.RESET_ALL}\n")
                return True

        # Verifica comandos restritos da configuração
        if hasattr(self, 'executor') and hasattr(self.executor, 'restricted_commands'):
            for restricted in self.executor.restricted_commands:
                if restricted.lower() in command_lower:
                    print(f"\n{Fore.RED}{'=' * 70}{Style.RESET_ALL}")
                    print(f"{Fore.RED}{Style.BRIGHT}⚠  COMANDO BLOQUEADO POR CONFIGURAÇÃO{Style.RESET_ALL}")
                    print(f"{Fore.RED}{'=' * 70}{Style.RESET_ALL}\n")
                    print(f"{Fore.YELLOW}Padrão bloqueado:{Style.RESET_ALL} {Fore.RED}{restricted}{Style.RESET_ALL}")
                    print(f"\n{Fore.CYAN}ℹ  Este comando está na lista de restrições do config.yaml{Style.RESET_ALL}\n")
                    print(f"{Fore.YELLOW}Use 'help' para ver comandos disponíveis{Style.RESET_ALL}\n")
                    print(f"{Fore.RED}{'=' * 70}{Style.RESET_ALL}\n")
                    return True

        return False

    def process_command(self, command: str):
        """
        Processa um comando usando o parser.

        Args:
            command: String com o comando a ser processado
        """
        # Remove espaços extras
        command = command.strip()

        # Ignora linhas vazias
        if not command:
            return

        # Verifica comandos restritos ANTES de tentar fazer parsing
        if self._check_restricted_command(command):
            return

        # Adiciona ao histórico
        self.history.append(command)

        # Faz parsing do comando
        try:
            ast = self.parser.parse(command, debug=self.debug_mode)

            if ast is None:
                # O parser ja imprime o erro
                return

            # Exibe AST em modo debug
            if self.debug_mode:
                print(f"\n{Fore.BLUE}[DEBUG - AST]{Style.RESET_ALL}")
                print(f"  Tipo: {type(ast).__name__}")
                print(f"  Repr: {ast}")
                import json
                print(f"  Dict: {json.dumps(ast.to_dict(), indent=2)}")
                print()

            # Executa o comando baseado no tipo da AST
            self.execute_ast(ast)

        except Exception as e:
            print(f"{Fore.RED}Erro ao processar comando: {e}{Style.RESET_ALL}")
            if self.debug_mode:
                import traceback
                traceback.print_exc()
    
    def execute_ast(self, ast):
        """
        Executa um nó da AST.
        
        Args:
            ast: Nó da AST a ser executado
        """
        # Pega o nome da classe para comparação
        class_name = type(ast).__name__
        
        # Comandos de controle já implementados 
        if class_name == 'ExitCommand':
            print(f"{Fore.YELLOW}Encerrando TermIA... Até logo!{Style.RESET_ALL}")
            self.running = False
            return
        
        elif class_name == 'ClearCommand':
            os.system('clear' if os.name != 'nt' else 'cls')
            return
        
        elif class_name == 'HistoryCommand':
            self.show_history_ast(ast)
            return
        
        elif class_name == 'HelpCommand':
            self.show_help_ast(ast)
            return
        
        # Comandos de SO
        elif class_name == 'PwdCommand':
            self.execute_pwd()
            return

        elif class_name == 'LSCommand':
            self.execute_ls(ast)
            return

        elif class_name == 'CDCommand':
            self.execute_cd(ast)
            return

        elif class_name == 'MkdirCommand':
            self.execute_mkdir(ast)
            return

        elif class_name == 'CatCommand':
            self.execute_cat(ast)
            return
        
        # Comandos de IA
        elif class_name == 'IAAskCommand':
            self.execute_ia_ask(ast)
            return

        elif class_name == 'IASummarizeCommand':
            self.execute_ia_summarize(ast)
            return

        elif class_name == 'IACodeExplainCommand':
            self.execute_ia_codeexplain(ast)
            return

        elif class_name == 'IATranslateCommand':
            self.execute_ia_translate(ast)
            return
        
        # Comando desconhecido
        else:
            print(f"{Fore.RED}Erro: tipo de comando desconhecido: {class_name}{Style.RESET_ALL}")
    
    def show_history_ast(self, ast: HistoryCommand):
        "Mostra o histórico usando o nó AST."
        n = ast.count

        # Get history from file if enhanced mode
        if self.enhanced_mode:
            try:
                with open('.termia_history', 'r', encoding='utf-8') as f:
                    lines = f.readlines()

                # FileHistory format: lines with '+' prefix are commands, '#' are timestamps
                all_history = []
                for line in lines:
                    line = line.strip()
                    if line.startswith('+'):
                        # Remove '+' prefix and add to history
                        all_history.append(line[1:].strip())

                history_to_show = all_history[-n:]
            except Exception:
                history_to_show = self.history[-n:]
        else:
            history_to_show = self.history[-n:]

        print(f"\n{Fore.CYAN}Histórico (últimos {n} comandos):{Style.RESET_ALL}")
        for i, cmd in enumerate(history_to_show, 1):
            print(f"{Fore.YELLOW}{i:3d}.{Style.RESET_ALL} {cmd}")
        print()
    
    def show_help_ast(self, ast: HelpCommand):
        "Mostra ajuda usando o nó AST."
        if ast.command is None:
            # Ajuda geral
            help_text = f"""
{Fore.CYAN}{Style.BRIGHT}Comandos Disponíveis:{Style.RESET_ALL}

{Fore.YELLOW}Sistema Operacional:{Style.RESET_ALL}
  ls [opções] [caminho]          - Lista arquivos e diretórios
  cd [caminho]                   - Muda de diretório
  mkdir [-p] <dir>               - Cria diretório
  pwd                            - Mostra diretório atual
  cat <arquivo>                  - Exibe conteúdo de arquivo

{Fore.YELLOW}Inteligência Artificial:{Style.RESET_ALL}
  ia ask "<pergunta>"            - Faz pergunta à IA (help ask)
  ia summarize "<texto>"         - Resume texto (help summarize)
  ia codeexplain <arquivo>       - Explica código (help codeexplain)
  ia translate "<texto>" --to pt - Traduz texto (help translate)

{Fore.YELLOW}Controle:{Style.RESET_ALL}
  history [n]                    - Mostra histórico
  clear                          - Limpa tela
  help [comando]                 - Mostra ajuda detalhada
  exit                           - Sai do terminal

{Fore.GREEN}Ajuda detalhada:{Style.RESET_ALL}
  help ia            - Visão geral dos comandos IA
  help ask           - Ajuda detalhada do ia ask
  help summarize     - Ajuda detalhada do ia summarize
  help codeexplain   - Ajuda detalhada do ia codeexplain
  help translate     - Ajuda detalhada do ia translate

{Fore.BLUE}Modo debug: execute com --debug{Style.RESET_ALL}

{Fore.CYAN}Exemplos:{Style.RESET_ALL}
  ia ask "O que é compilador?"
  ia summarize "texto aqui" --length short
  ia codeexplain main.py
  ia translate "Hello" --to pt

{Fore.YELLOW}Nota:{Style.RESET_ALL}
  TermIA não suporta shell substitution $(cmd), pipes |, ou redirecionamento >
  Este é um terminal educacional focado em análise léxica e sintática
"""
            print(help_text)
        else:
            # Ajuda específica
            cmd = ast.command
            helps = {
                'ls': 'ls [opções] [caminho]\n  Lista arquivos e diretórios\n  Opções: -a (todos), -l (detalhado), -h (legível)',
                'cd': 'cd [caminho]\n  Muda o diretório de trabalho\n  Exemplos: cd .., cd ~, cd /home',
                'mkdir': 'mkdir [-p] <diretório>\n  Cria um novo diretório\n  -p: cria diretórios pais se necessário',
                'pwd': 'pwd\n  Mostra o diretório de trabalho atual',
                'cat': 'cat <arquivo>\n  Exibe o conteúdo de um arquivo',
                'ia': '''ia <subcomando>
  Comandos de IA disponíveis:

  ia ask "<pergunta>"
    Faz uma pergunta à IA
    Exemplo: ia ask "O que é Python?"

  ia summarize "<texto>" [--length short|medium|long]
    Resume um texto fornecido
    Exemplo: ia summarize "texto longo aqui" --length short

  ia codeexplain <arquivo>
    Explica o código de um arquivo
    Exemplo: ia codeexplain main.py
    NOTA: Requer um caminho de arquivo, não uma string

  ia translate "<texto>" --to <idioma>
    Traduz texto para outro idioma
    Exemplo: ia translate "Hello world" --to pt
    Idiomas: pt, en, es, fr, de, it, ja, zh

  IMPORTANTE:
    TermIA não suporta shell substitution como $(cat file)
    Para resumir conteúdo de arquivo, use ia codeexplain
    ou copie e cole o texto diretamente

  Para ajuda detalhada: help ask, help summarize, etc.''',
                # IA Subcommands
                'ask': '''ia ask "<pergunta>"
  Faz uma pergunta à IA e recebe uma resposta

  SINTAXE:
    ia ask "<sua pergunta>"

  EXEMPLOS:
    ia ask "O que é Python?"
    ia ask "Explique o que é um compilador"
    ia ask "Qual a diferença entre léxico e sintático?"

  NOTAS:
    • A pergunta deve estar entre aspas
    • Respostas em texto puro otimizado para terminal
    • Não suporta shell substitution $(cmd)''',
                'summarize': '''ia summarize "<texto>" [--length <tamanho>]
  Resume um texto fornecido

  SINTAXE:
    ia summarize "<texto a resumir>"
    ia summarize "<texto a resumir>" --length <tamanho>

  OPÇÕES:
    --length short   - Resumo curto (2-3 frases)
    --length medium  - Resumo médio (1 parágrafo) [padrão]
    --length long    - Resumo detalhado (múltiplos parágrafos)

  EXEMPLOS:
    ia summarize "Python é uma linguagem..." --length short
    ia summarize "Este texto fala sobre compiladores..."

  NOTAS:
    • O texto deve estar entre aspas
    • Não use $(cat arquivo) - não é suportado
    • Para arquivos de código, use: ia codeexplain arquivo''',
                'codeexplain': '''ia codeexplain <arquivo>
  Explica o código de um arquivo

  SINTAXE:
    ia codeexplain <caminho_do_arquivo>

  EXEMPLOS:
    ia codeexplain main.py
    ia codeexplain src/parser.py
    ia codeexplain ../outro_arquivo.py

  NOTAS:
    • NÃO use aspas em volta do nome do arquivo
    • O arquivo deve existir no sistema
    • Suporta caminhos relativos e absolutos
    • Código truncado em 2000 caracteres para evitar limites
    • Saída otimizada para terminal (sem markdown)

  ERROS COMUNS:
    ✗ ia codeexplain "main.py"     (não use aspas)
    ✗ ia codeexplain --length      (--length é para summarize)
    ✓ ia codeexplain main.py       (correto!)''',
                'translate': '''ia translate "<texto>" --to <idioma>
  Traduz texto para outro idioma

  SINTAXE:
    ia translate "<texto a traduzir>" --to <código_idioma>

  IDIOMAS SUPORTADOS:
    pt - Português    en - Inglês      es - Espanhol
    fr - Francês      de - Alemão      it - Italiano
    ja - Japonês      zh - Chinês      ru - Russo
    ar - Árabe

  EXEMPLOS:
    ia translate "Hello world" --to pt
    ia translate "Bom dia" --to en
    ia translate "Good morning" --to es

  NOTAS:
    • O texto deve estar entre aspas
    • O código do idioma usa 2 letras
    • Apenas a tradução é retornada (sem explicações)
    • Não suporta shell substitution $(cmd)''',
                'history': 'history [n]\n  Mostra os últimos n comandos (padrão: 10)',
                'clear': 'clear\n  Limpa a tela do terminal',
                'help': 'help [comando]\n  Mostra ajuda geral ou sobre um comando específico\n  Também funciona com subcomandos: help ask, help translate',
                'exit': 'exit\n  Encerra o TermIA'
            }
            
            # Normalize command name (lowercase)
            cmd_lower = cmd.lower() if isinstance(cmd, str) else str(cmd).lower()

            if cmd_lower in helps:
                print(f"\n{Fore.CYAN}{helps[cmd_lower]}{Style.RESET_ALL}\n")
            else:
                print(f"\n{Fore.RED}Comando '{cmd}' não encontrado{Style.RESET_ALL}")
                print(f"\n{Fore.YELLOW}Comandos disponíveis:{Style.RESET_ALL}")
                print(f"  OS: ls, cd, mkdir, pwd, cat")
                print(f"  IA: ask, summarize, codeexplain, translate")
                print(f"  Controle: history, clear, help, exit")
                print(f"\n{Fore.CYAN}Dica:{Style.RESET_ALL} Use 'help' para ver a lista completa")
                print(f"{Fore.CYAN}      Para comandos IA: help ask, help translate, etc.{Style.RESET_ALL}\n")

    # ==================== Executores de Comandos do SO ====================

    def execute_pwd(self):
        """Executa o comando pwd."""
        try:
            result = self.executor.execute_pwd()
            print(f"{Fore.CYAN}{result}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Erro ao executar pwd: {e}{Style.RESET_ALL}")

    def execute_ls(self, ast: LSCommand):
        """Executa o comando ls."""
        try:
            result = self.executor.execute_ls(options=ast.options, path=ast.path)
            print(result)
        except SecurityException as e:
            print(f"{Fore.RED}⚠ Erro de Segurança: {e}{Style.RESET_ALL}")
        except FileNotFoundError as e:
            print(f"{Fore.RED}{e}{Style.RESET_ALL}")
        except PermissionError as e:
            print(f"{Fore.RED}{e}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Erro ao executar ls: {e}{Style.RESET_ALL}")

    def execute_cd(self, ast: CDCommand):
        """Executa o comando cd."""
        try:
            result = self.executor.execute_cd(path=ast.path)
            # Atualiza o current_dir do TermIA também
            self.current_dir = self.executor.current_dir
            print(f"{Fore.GREEN}{result}{Style.RESET_ALL}")
        except SecurityException as e:
            print(f"{Fore.RED}⚠ Erro de Segurança: {e}{Style.RESET_ALL}")
        except FileNotFoundError as e:
            print(f"{Fore.RED}{e}{Style.RESET_ALL}")
        except NotADirectoryError as e:
            print(f"{Fore.RED}{e}{Style.RESET_ALL}")
        except PermissionError as e:
            print(f"{Fore.RED}{e}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Erro ao executar cd: {e}{Style.RESET_ALL}")

    def execute_mkdir(self, ast: MkdirCommand):
        """Executa o comando mkdir."""
        try:
            result = self.executor.execute_mkdir(path=ast.path, create_parents=ast.create_parents)
            print(f"{Fore.GREEN}{result}{Style.RESET_ALL}")
        except SecurityException as e:
            print(f"{Fore.RED}⚠ Erro de Segurança: {e}{Style.RESET_ALL}")
        except FileExistsError as e:
            print(f"{Fore.RED}{e}{Style.RESET_ALL}")
        except PermissionError as e:
            print(f"{Fore.RED}{e}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Erro ao executar mkdir: {e}{Style.RESET_ALL}")

    def execute_cat(self, ast: CatCommand):
        """Executa o comando cat."""
        try:
            result = self.executor.execute_cat(filepath=ast.filepath)
            print(result)
        except SecurityException as e:
            print(f"{Fore.RED}⚠ Erro de Segurança: {e}{Style.RESET_ALL}")
        except FileNotFoundError as e:
            print(f"{Fore.RED}{e}{Style.RESET_ALL}")
        except IsADirectoryError as e:
            print(f"{Fore.RED}{e}{Style.RESET_ALL}")
        except PermissionError as e:
            print(f"{Fore.RED}{e}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Erro ao executar cat: {e}{Style.RESET_ALL}")

    # ==================== Executores de Comandos de IA ====================

    def execute_ia_ask(self, ast: IAAskCommand):
        """Executa o comando ia ask."""
        try:
            print(f"{Fore.YELLOW}[IA] Processando pergunta...{Style.RESET_ALL}")
            result = self.ai_executor.execute_ia_ask(ast.question)
            print(f"{Fore.CYAN}{result}{Style.RESET_ALL}")
        except AIException as e:
            print(f"{Fore.RED}Erro de IA: {e}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Erro ao executar ia ask: {e}{Style.RESET_ALL}")

    def execute_ia_summarize(self, ast: IASummarizeCommand):
        """Executa o comando ia summarize."""
        try:
            print(f"{Fore.YELLOW}[IA] Resumindo texto (tamanho: {ast.length})...{Style.RESET_ALL}")
            result = self.ai_executor.execute_ia_summarize(ast.text, ast.length)
            print(f"{Fore.CYAN}Resumo:{Style.RESET_ALL}")
            print(f"{result}")
        except AIException as e:
            print(f"{Fore.RED}Erro de IA: {e}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Erro ao executar ia summarize: {e}{Style.RESET_ALL}")

    def execute_ia_codeexplain(self, ast: IACodeExplainCommand):
        """Executa o comando ia codeexplain."""
        try:
            print(f"{Fore.YELLOW}[IA] Analisando codigo em '{ast.filepath}'...{Style.RESET_ALL}")
            # Resolve path relative to executor's current dir
            filepath = os.path.join(self.executor.current_dir, ast.filepath)
            result = self.ai_executor.execute_ia_codeexplain(filepath)
            print(f"{Fore.CYAN}Explicacao do codigo:{Style.RESET_ALL}")
            print(f"{result}")
        except AIException as e:
            print(f"{Fore.RED}Erro de IA: {e}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Erro ao executar ia codeexplain: {e}{Style.RESET_ALL}")

    def execute_ia_translate(self, ast: IATranslateCommand):
        """Executa o comando ia translate."""
        try:
            print(f"{Fore.YELLOW}[IA] Traduzindo para {ast.target_language}...{Style.RESET_ALL}")
            result = self.ai_executor.execute_ia_translate(ast.text, ast.target_language)
            print(f"{Fore.CYAN}Traducao:{Style.RESET_ALL}")
            print(f"{result}")
        except AIException as e:
            print(f"{Fore.RED}Erro de IA: {e}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Erro ao executar ia translate: {e}{Style.RESET_ALL}")

    def run(self):
        "Loop principal do terminal."
        self.print_banner()

        while self.running:
            try:
                # Lê comando do usuário (com ou sem enhanced mode)
                if self.enhanced_mode:
                    command = self.input_handler.get_input(self.get_prompt())
                else:
                    command = input(self.get_prompt())

                # Processa comando
                self.process_command(command)

            except KeyboardInterrupt:
                # Ctrl+C
                print(f"\n{Fore.YELLOW}Use 'exit' para sair{Style.RESET_ALL}")
            except EOFError:
                print(f"\n{Fore.YELLOW}Encerrando...{Style.RESET_ALL}")
                break
            except Exception as e:
                print(f"{Fore.RED}Erro inesperado: {e}{Style.RESET_ALL}")
                if self.debug_mode:
                    import traceback
                    traceback.print_exc()


def main():
    "Função principal."
    
    # Verifica argumentos de linha de comando
    debug_mode = '--debug' in sys.argv or '-d' in sys.argv
    
    if '--help' in sys.argv or '-h' in sys.argv:
        print("""
TermIA - Terminal Inteligente

Uso: python main.py [opções]

Opções:
  --debug, -d    Ativa modo debug (mostra tokens e AST)
  --help, -h     Mostra esta mensagem
  --version, -v  Mostra versão
        """)
        sys.exit(0)
    
    if '--version' in sys.argv or '-v' in sys.argv:
        print("TermIA v2.0 - Terminal Inteligente")
        print("Autores: Argéu e Henrique")
        print("Projeto de Compiladores - UNIFEI 2025")
        sys.exit(0)
    
    # Cria e executa o terminal
    terminal = TermIA(debug_mode=debug_mode)
    terminal.run()


if __name__ == '__main__':
    main()