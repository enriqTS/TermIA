"""
TermIA - Analisador Sintático
Este módulo implementa o parser usando PLY (Python Lex-Yacc)
para analisar a sintaxe dos comandos do TermIA.
"""

import ply.yacc as yacc
from lexer import TermIALexer
from ast_nodes import (
    # OS Commands
    LSCommand, CDCommand, MkdirCommand, PwdCommand, CatCommand,
    # IA Commands
    IAAskCommand, IASummarizeCommand, IACodeExplainCommand, IATranslateCommand,
    # Control Commands
    HistoryCommand, ClearCommand, HelpCommand, ExitCommand
)


class TermIAParser:
    """
    Analisador sintático para o TermIA.
    Constrói uma AST (Abstract Syntax Tree) a partir dos tokens.
    """
    
    def __init__(self):
        "Inicializa o parser"
        self.lexer = TermIALexer()
        self.tokens = self.lexer.tokens
        self.parser = None
        self.build()
    
    def build(self, **kwargs):
        "Constrói o parser"
        self.parser = yacc.yacc(module=self, **kwargs)
    
    # ==================== Regra Inicial ====================
    
    def p_command(self, p):
        """command : os_command
                   | ia_command
                   | control_command"""
        p[0] = p[1]
    
    # ==================== Comandos do SO ====================
    
    def p_os_command(self, p):
        """os_command : ls_command
                      | cd_command
                      | mkdir_command
                      | pwd_command
                      | cat_command"""
        p[0] = p[1]
    
    # --- Comando LS ---
    
    def p_ls_command_full(self, p):
        "ls_command : LS OPTION_SHORT path"
        p[0] = LSCommand(options=p[2], path=p[3])
    
    def p_ls_command_with_path(self, p):
        "ls_command : LS path"
        p[0] = LSCommand(path=p[2])
    
    def p_ls_command_with_option(self, p):
        "ls_command : LS OPTION_SHORT"
        p[0] = LSCommand(options=p[2])
    
    def p_ls_command_simple(self, p):
        "ls_command : LS"
        p[0] = LSCommand()
    
    # --- Comando CD ---
    
    def p_cd_command_with_path(self, p):
        "cd_command : CD path"
        p[0] = CDCommand(path=p[2])
    
    def p_cd_command_simple(self, p):
        "cd_command : CD"
        p[0] = CDCommand()
    
    # --- Comando MKDIR ---
    
    def p_mkdir_command_with_p(self, p):
        "mkdir_command : MKDIR OPTION_SHORT path"
        create_parents = 'p' in p[2]
        p[0] = MkdirCommand(path=p[3], create_parents=create_parents)
    
    def p_mkdir_command_simple(self, p):
        "mkdir_command : MKDIR path"
        p[0] = MkdirCommand(path=p[2])
    
    # --- Comando PWD ---
    
    def p_pwd_command(self, p):
        "pwd_command : PWD"
        p[0] = PwdCommand()
    
    # --- Comando CAT ---
    
    def p_cat_command(self, p):
        "cat_command : CAT path"
        p[0] = CatCommand(filepath=p[2])
    
    # ==================== Comandos de IA ====================
    
    def p_ia_command(self, p):
        "ia_command : IA ia_subcommand"
        p[0] = p[2]
    
    def p_ia_subcommand(self, p):
        """ia_subcommand : ia_ask
                         | ia_summarize
                         | ia_codeexplain
                         | ia_translate"""
        p[0] = p[1]
    
    # --- IA Ask ---
    
    def p_ia_ask(self, p):
        "ia_ask : ASK STRING"
        p[0] = IAAskCommand(question=p[2])
    
    # --- IA Summarize ---
    
    def p_ia_summarize_with_length(self, p):
        "ia_summarize : SUMMARIZE STRING LONG_OPTION IDENTIFIER"
        # Verifica se a opção é --length
        if p[3] == 'length':
            length = p[4]
        else:
            length = 'short'
        p[0] = IASummarizeCommand(text=p[2], length=length)
    
    def p_ia_summarize_simple(self, p):
        "ia_summarize : SUMMARIZE STRING"
        p[0] = IASummarizeCommand(text=p[2])
    
    # --- IA Code Explain ---
    
    def p_ia_codeexplain(self, p):
        "ia_codeexplain : CODEEXPLAIN path"
        p[0] = IACodeExplainCommand(filepath=p[2])
    
    # --- IA Translate ---
    
    def p_ia_translate(self, p):
        "ia_translate : TRANSLATE STRING LONG_OPTION IDENTIFIER"
        # Verifica se a opção é --to
        if p[3] == 'to':
            target_lang = p[4]
        else:
            target_lang = 'en'
        p[0] = IATranslateCommand(text=p[2], target_language=target_lang)
    
    # ==================== Comandos de Controle ====================
    
    def p_control_command(self, p):
        """control_command : history_command
                           | clear_command
                           | help_command
                           | exit_command"""
        p[0] = p[1]
    
    # --- History ---
    
    def p_history_command_with_count(self, p):
        "history_command : HISTORY NUMBER"
        p[0] = HistoryCommand(count=p[2])
    
    def p_history_command_simple(self, p):
        "history_command : HISTORY"
        p[0] = HistoryCommand()
    
    # --- Clear ---
    
    def p_clear_command(self, p):
        "clear_command : CLEAR"
        p[0] = ClearCommand()
    
    # --- Help ---
    
    def p_help_command_with_topic(self, p):
        "help_command : HELP command_name"
        p[0] = HelpCommand(command=p[2])
    
    def p_help_command_simple(self, p):
        "help_command : HELP"
        p[0] = HelpCommand()
    
    # --- Exit ---
    
    def p_exit_command(self, p):
        "exit_command : EXIT"
        p[0] = ExitCommand()
    
    # ==================== Regras Auxiliares ====================
    
    def p_path(self, p):
        """path : PATH
                | IDENTIFIER
                | DOT
                | DOTDOT
                | TILDE"""
        p[0] = str(p[1])
    
    def p_command_name(self, p):
        """command_name : LS
                        | CD
                        | MKDIR
                        | PWD
                        | CAT
                        | IA
                        | HISTORY
                        | CLEAR
                        | HELP
                        | EXIT
                        | IDENTIFIER"""
        p[0] = p[1]
    
    # ==================== Tratamento de Erros ====================
    
    def p_error(self, p):
        "Tratamento de erro sintático."
        if p:
            # Mensagens específicas para erros comuns
            if p.type == 'MKDIR':
                print(f"Erro de sintaxe: comando 'mkdir' requer um caminho")
                print(f"  Uso: mkdir <diretório>  ou  mkdir -p <diretório>")
            elif p.type == 'CAT':
                print(f"Erro de sintaxe: comando 'cat' requer um arquivo")
                print(f"  Uso: cat <arquivo>")
            else:
                print(f"Erro de sintaxe no token '{p.value}' (tipo: {p.type}) na posição {p.lexpos}")
            # Tenta recuperar do erro descartando o token
            self.parser.errok()
        else:
            print("Erro de sintaxe: comando incompleto")
            print("  Digite 'help' para ver os comandos disponíveis")
    
    # ==================== Métodos Públicos ====================
    
    def parse(self, text: str, debug: bool = False):
        """
        Analisa um comando e retorna a AST.
        
        Args:
            text: String contendo o comando a ser analisado
            debug: Se True, imprime informações de debug
            
        Returns:
            Nó raiz da AST ou None em caso de erro
        """
        try:
            # Primeiro tokeniza
            self.lexer.lexer.input(text)
            
            if debug:
                print(f"\nTokenizando: '{text}'")
                print("-" * 50)
                self.lexer.lexer.input(text)
                for tok in self.lexer.lexer:
                    print(f"  {tok.type:15s} -> {repr(tok.value)}")
                print("-" * 50)
                
                # Reset lexer para parsing
                self.lexer.lexer.input(text)
            
            # Depois faz parsing
            result = self.parser.parse(text, lexer=self.lexer.lexer, debug=debug)
            
            return result
            
        except Exception as e:
            print(f"Erro ao fazer parsing: {e}")
            return None
    
    def parse_and_print(self, text: str):
        """
        Analisa um comando e imprime a AST (útil para debug).
        
        Args:
            text: String contendo o comando a ser analisado
        """
        print(f"\nParsing: '{text}'")
        print("=" * 60)
        
        ast = self.parse(text)
        
        if ast:
            print("\nAST gerada:")
            print(ast)
            print("\nRepresentação em dict:")
            import json
            print(json.dumps(ast.to_dict(), indent=2))
        else:
            print("Falha ao fazer parsing")
        
        print("=" * 60)


def main():
    "Função principal para testes do parser."
    parser = TermIAParser()
    
    # Casos de teste
    test_cases = [
        # Comandos de SO
        'ls',
        'ls -la',
        'ls /home/user',
        'ls ./home/user',
        'ls ..',
        'ls -lah /var/log',
        'cd ..',
        'cd /home',
        'cd',
        'mkdir test',
        'mkdir -p projects/2024/termia',
        'pwd',
        'cat README.md',
        
        # Comandos de IA
        'ia ask "O que é Python?"',
        'ia summarize "Lorem ipsum dolor sit amet"',
        'ia summarize "texto longo aqui" --length medium',
        'ia codeexplain main.py',
        'ia translate "Hello World" --to pt',
        
        # Comandos de controle
        'history',
        'history 20',
        'clear',
        'help',
        'help ls',
        'exit',
    ]
    
    print("=" * 70)
    print("TESTE DO PARSER - TermIA")
    print("=" * 70)
    
    success_count = 0
    for i, test in enumerate(test_cases, 1):
        print(f"\n[Teste {i}/{len(test_cases)}]")
        result = parser.parse(test)
        if result:
            print(f"✓ '{test}' -> {result}")
            success_count += 1
        else:
            print(f"✗ '{test}' -> FALHOU")
    
    print("\n" + "=" * 70)
    print(f"Resultado: {success_count}/{len(test_cases)} testes passaram")
    print("=" * 70)


if __name__ == '__main__':
    main()