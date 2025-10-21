#!/usr/bin/env python3
import sys
import os

# Adiciona o diretório src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from lexer import TermIALexer

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
        RESET = ''
    
    class Style:
        BRIGHT = ''
        RESET_ALL = ''


class TermIA:
    """Classe principal do TermIA."""
    
    def __init__(self):
        """Inicializa o TermIA."""
        self.lexer = TermIALexer()
        self.history = []
        self.running = True
        self.current_dir = os.getcwd()
    
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
║         {Fore.YELLOW}Terminal Inteligente - Versão 1.0{Fore.CYAN}          ║
║         {Fore.GREEN}Projeto de Compiladores - UNIFEI{Fore.CYAN}           ║
║                                                       ║
╚═══════════════════════════════════════════════════════╝{Style.RESET_ALL}

{Fore.YELLOW}Digite 'help' para ajuda ou 'exit' para sair{Style.RESET_ALL}
{Fore.GREEN}Status: Lexer ativo | Parser: em desenvolvimento{Style.RESET_ALL}
"""
        print(banner)
    
    def get_prompt(self):
        """Retorna o prompt do terminal."""
        # Mostra apenas o nome do diretório atual, não o caminho completo
        dir_name = os.path.basename(self.current_dir)
        if not dir_name:
            dir_name = self.current_dir
        return f"{Fore.GREEN}{dir_name}{Fore.CYAN} TermIA>{Style.RESET_ALL} "
    
    def process_command(self, command: str):
        """
        Processa um comando.
        
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
        
        # Comandos internos (não precisam do parser ainda)
        if command == 'exit':
            print(f"{Fore.YELLOW}Encerrando TermIA... Até logo!{Style.RESET_ALL}")
            self.running = False
            return
        
        if command == 'clear':
            os.system('clear' if os.name != 'nt' else 'cls')
            return
        
        if command.startswith('history'):
            self.show_history(command)
            return
        
        if command.startswith('help'):
            self.show_help(command)
            return
        
        # Para outros comandos, mostra a tokenização (debug mode)
        print(f"\n{Fore.CYAN}[DEBUG - Lexer] Tokenizando comando...{Style.RESET_ALL}")
        try:
            tokens = self.lexer.tokenize_to_list(command)
            print(f"{Fore.GREEN}✓ Tokens reconhecidos:{Style.RESET_ALL}")
            for i, token in enumerate(tokens, 1):
                print(f"  {i}. {Fore.YELLOW}{token.type:15s}{Style.RESET_ALL} → {Fore.CYAN}{repr(token.value)}{Style.RESET_ALL}")
            
            print(f"\n{Fore.YELLOW}⚠ Parser e Executor ainda não implementados.{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}  Este comando será executado nas próximas versões.{Style.RESET_ALL}\n")
            
        except Exception as e:
            print(f"{Fore.RED}✗ Erro ao tokenizar: {e}{Style.RESET_ALL}")
    
    def show_history(self, command: str):
        """Mostra o histórico de comandos."""
        parts = command.split()
        n = 10  # padrão
        
        if len(parts) > 1:
            try:
                n = int(parts[1])
            except ValueError:
                print(f"{Fore.RED}Erro: número inválido{Style.RESET_ALL}")
                return
        
        print(f"\n{Fore.CYAN}Histórico (últimos {n} comandos):{Style.RESET_ALL}")
        for i, cmd in enumerate(self.history[-n:], 1):
            print(f"{Fore.YELLOW}{i:3d}.{Style.RESET_ALL} {cmd}")
        print()
    
    def show_help(self, command: str):
        """Mostra ajuda sobre comandos."""
        parts = command.split()
        
        if len(parts) == 1:
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
"""
            print(help_text)
        else:
            # Ajuda específica
            cmd = parts[1]
            helps = {
                'ls': 'ls [opções] [caminho]\n  Lista arquivos e diretórios\n  Opções: -a (todos), -l (detalhado), -h (legível)',
                'cd': 'cd [caminho]\n  Muda o diretório de trabalho\n  Exemplos: cd .., cd ~, cd /home',
                'mkdir': 'mkdir [-p] <diretório>\n  Cria um novo diretório\n  -p: cria diretórios pais se necessário',
                'pwd': 'pwd\n  Mostra o diretório de trabalho atual',
                'cat': 'cat <arquivo>\n  Exibe o conteúdo de um arquivo',
                'ia': 'ia <subcomando>\n  Comandos de IA: ask, summarize, codeexplain, translate',
                'history': 'history [n]\n  Mostra os últimos n comandos (padrão: 10)',
                'clear': 'clear\n  Limpa a tela do terminal',
                'help': 'help [comando]\n  Mostra ajuda geral ou sobre um comando específico',
                'exit': 'exit\n  Encerra o TermIA'
            }
            
            if cmd in helps:
                print(f"\n{Fore.CYAN}{helps[cmd]}{Style.RESET_ALL}\n")
            else:
                print(f"{Fore.RED}Comando '{cmd}' não encontrado{Style.RESET_ALL}")
    
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


def main():
    """Função principal."""
    # Verifica versão do Python
    if sys.version_info < (3, 8):
        print("Erro: TermIA requer Python 3.8 ou superior")
        sys.exit(1)
    
    # Cria e executa o terminal
    terminal = TermIA()
    terminal.run()


if __name__ == '__main__':
    main()