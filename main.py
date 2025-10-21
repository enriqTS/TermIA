#!/usr/bin/env python3
"""
TermIA - Terminal Inteligente
Arquivo principal para executar o terminal.

Versão 2.0 - com Lexer e Parser integrados.
Executor será implementado na próxima semana.

Autor: [Seu Nome]
Data: Outubro 2024
Disciplina: ECOI26 - Compiladores
Professor: Walter Aoiama Nagai
"""

import sys
import os

# Adiciona o diretório src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.parser import TermIAParser
from src.ast_nodes import (
    LSCommand, CDCommand, MkdirCommand, PwdCommand, CatCommand,
    IAAskCommand, IASummarizeCommand, IACodeExplainCommand, IATranslateCommand,
    HistoryCommand, ClearCommand, HelpCommand, ExitCommand
)

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
    """Classe principal do TermIA."""
    
    def __init__(self, debug_mode=False):
        """Inicializa o TermIA."""
        self.parser = TermIAParser()
        self.history = []
        self.running = True
        self.current_dir = os.getcwd()
        self.debug_mode = debug_mode
    
    def print_banner(self):
        """Imprime o banner de bienvenida."""
        banner = f"""
{Fore.CYAN}{Style.BRIGHT}╔═══════════════════════════════════════════════════════╗
║                                                       ║
║   {Fore.MAGENTA}████████╗███████╗██████╗ ███╗   ███╗██╗ █████╗ {Fore.CYAN}  ║
║   {Fore.MAGENTA}╚══██╔══╝██╔════╝██╔══██╗████╗ ████║██║██╔══██╗{Fore.CYAN}  ║
║   {Fore.MAGENTA}   ██║   █████╗  ██████╔╝██╔████╔██║██║███████║{Fore.CYAN}  ║
║   {Fore.MAGENTA}   ██║   ██╔══╝  ██╔══██╗██║╚██╔╝██║██║██╔══██║{Fore.CYAN}  ║
║   {Fore.MAGENTA}   ██║   ███████╗██║  ██║██║ ╚═╝ ██║██║██║  ██║{Fore.CYAN}  ║
║   {Fore.MAGENTA}   ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝╚═╝  ╚═╝{Fore.CYAN}  ║
║                                                       ║
║         {Fore.YELLOW}Terminal Inteligente - Versão 2.0{Fore.CYAN}          ║
║         {Fore.GREEN}Projeto de Compiladores - UNIFEI{Fore.CYAN}           ║
║                                                       ║
╚═══════════════════════════════════════════════════════╝{Style.RESET_ALL}

{Fore.YELLOW}Digite 'help' para ajuda ou 'exit' para sair{Style.RESET_ALL}
{Fore.GREEN}Status: Lexer ✓ | Parser ✓ | Executor: em desenvolvimento{Style.RESET_ALL}
"""
        print(banner)
    
    def get_prompt(self):
        """Retorna o prompt do terminal."""
        # Mostra apenas o nome do diretório atual
        dir_name = os.path.basename(self.current_dir)
        if not dir_name:
            dir_name = self.current_dir
        return f"{Fore.GREEN}{dir_name}{Fore.CYAN} TermIA>{Style.RESET_ALL} "
    
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
        
        # Adiciona ao histórico
        self.history.append(command)
        
        # Faz parsing do comando
        try:
            ast = self.parser.parse(command, debug=self.debug_mode)
            
            if ast is None:
                print(f"{Fore.RED}Erro: comando não reconhecido ou sintaxe inválida{Style.RESET_ALL}")
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
        # Comandos de controle (implementados)
        if isinstance(ast, ExitCommand):
            print(f"{Fore.YELLOW}Encerrando TermIA... Até logo!{Style.RESET_ALL}")
            self.running = False
            return
        
        if isinstance(ast, ClearCommand):
            os.system('clear' if os.name != 'nt' else 'cls')
            return
        
        if isinstance(ast, HistoryCommand):
            self.show_history_ast(ast)
            return
        
        if isinstance(ast, HelpCommand):
            self.show_help_ast(ast)
            return
        
        # Outros comandos (ainda não implementados)
        if isinstance(ast, (LSCommand, CDCommand, MkdirCommand, PwdCommand, CatCommand)):
            print(f"{Fore.CYAN}[Parser OK] Comando reconhecido: {ast}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}⚠ Executor de comandos SO ainda não implementado.{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}  Este comando será executado na próxima versão.{Style.RESET_ALL}\n")
            return
        
        if isinstance(ast, (IAAskCommand, IASummarizeCommand, IACodeExplainCommand, IATranslateCommand)):
            print(f"{Fore.CYAN}[Parser OK] Comando IA reconhecido: {ast}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}⚠ Integração com IA ainda não implementada.{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}  Este comando será executado nas próximas semanas.{Style.RESET_ALL}\n")
            return
        
        # Comando não implementado
        print(f"{Fore.RED}Comando não implementado ainda: {type(ast).__name__}{Style.RESET_ALL}")
    
    def show_history_ast(self, ast: HistoryCommand):
        """Mostra o histórico usando o nó AST."""
        n = ast.count
        
        print(f"\n{Fore.CYAN}Histórico (últimos {n} comandos):{Style.RESET_ALL}")
        for i, cmd in enumerate(self.history[-n:], 1):
            print(f"{Fore.YELLOW}{i:3d}.{Style.RESET_ALL} {cmd}")
        print()
    
    def show_help_ast(self, ast: HelpCommand):
        """Mostra ajuda usando o nó AST."""
        if ast.command is None:
            # Ajuda geral
            help_text = f"""
{Fore.CYAN}{Style.BRIGHT}Comandos Disponíveis:{Style.RESET_ALL}

{Fore.YELLOW}Sistema Operacional:{Style.RESET_ALL}
  ls [opções] [caminho]      - Lista arquivos e diretórios
  cd [caminho]               - Muda de diretório
  mkdir [-p] <dir>           - Cria diretório
  pwd                        - Mostra diretório atual
  cat <arquivo>              - Exibe conteúdo de arquivo

{Fore.YELLOW}Inteligência Artificial:{Style.RESET_ALL}
  ia ask "<pergunta>"        - Faz pergunta à IA
  ia summarize "<texto>"     - Resume texto
  ia codeexplain <arquivo>   - Explica código
  ia translate "<texto>"     - Traduz texto

{Fore.YELLOW}Controle:{Style.RESET_ALL}
  history [n]                - Mostra histórico
  clear                      - Limpa tela
  help [comando]             - Mostra ajuda
  exit                       - Sai do terminal

{Fore.GREEN}Para mais informações: help <comando>{Style.RESET_ALL}
{Fore.BLUE}Modo debug: execute com --debug{Style.RESET_ALL}
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
                'ia': 'ia <subcomando>\n  Comandos de IA: ask, summarize, codeexplain, translate\n  Exemplo: ia ask "Sua pergunta aqui"',
                'history': 'history [n]\n  Mostra os últimos n comandos (padrão: 10)',
                'clear': 'clear\n  Limpa a tela do terminal',
                'help': 'help [comando]\n  Mostra ajuda geral ou sobre um comando específico',
                'exit': 'exit\n  Encerra o TermIA'
            }
            
            if cmd in helps:
                print(f"\n{Fore.CYAN}{helps[cmd]}{Style.RESET_ALL}\n")
            else:
                print(f"{Fore.RED}Comando '{cmd}' não encontrado{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}Use 'help' para ver todos os comandos{Style.RESET_ALL}")
    
    def run(self):
        """Loop principal do terminal."""
        self.print_banner()
        
        while self.running:
            try:
                # Lê comando do usuário
                command = input(self.get_prompt())
                
                # Processa comando
                self.process_command(command)
                
            except KeyboardInterrupt:
                # Ctrl+C
                print(f"\n{Fore.YELLOW}Use 'exit' para sair{Style.RESET_ALL}")
            except EOFError:
                # Ctrl+D
                print(f"\n{Fore.YELLOW}Encerrando...{Style.RESET_ALL}")
                break
            except Exception as e:
                print(f"{Fore.RED}Erro inesperado: {e}{Style.RESET_ALL}")
                if self.debug_mode:
                    import traceback
                    traceback.print_exc()


def main():
    """Função principal."""
    # Verifica versão do Python
    if sys.version_info < (3, 8):
        print("Erro: TermIA requer Python 3.8 ou superior")
        sys.exit(1)
    
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
        print("Projeto de Compiladores - UNIFEI 2024")
        sys.exit(0)
    
    # Cria e executa o terminal
    terminal = TermIA(debug_mode=debug_mode)
    terminal.run()


if __name__ == '__main__':
    main()