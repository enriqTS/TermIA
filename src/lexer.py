"""
TermIA - Analisador Léxico
Este módulo implementa o lexer usando PLY (Python Lex-Yacc)
para tokenizar comandos do TermIA.

Autor: [Seu Nome]
Data: Outubro 2024
Disciplina: ECOI26 - Compiladores
"""

import ply.lex as lex
from typing import Optional


class TermIALexer:
    """
    Analisador léxico para o TermIA.
    Tokeniza comandos do sistema operacional, comandos de IA e comandos de controle.
    """

    # Lista de tokens
    tokens = (
        # Comandos do Sistema Operacional
        'LS',
        'CD',
        'MKDIR',
        'PWD',
        'CAT',
        
        # Comandos de IA
        'IA',
        'ASK',
        'SUMMARIZE',
        'CODEEXPLAIN',
        'TRANSLATE',
        
        # Comandos de Controle
        'HISTORY',
        'CLEAR',
        'HELP',
        'EXIT',
        
        # Opções e argumentos
        'OPTION_SHORT',      # -a, -l, -p
        'LONG_OPTION',       # --length, --to
        
        # Literais
        'STRING',            # "texto entre aspas"
        'NUMBER',            # 123
        'PATH',              # /home/user, ./file, ../dir
        'IDENTIFIER',        # nome_arquivo, variavel
        
        # Símbolos especiais
        'DOT',               # .
        'DOTDOT',            # ..
        'TILDE',             # ~
        'SLASH',             # /
    )

    # Palavras reservadas (keywords)
    reserved = {
        # Sistema Operacional
        'ls': 'LS',
        'cd': 'CD',
        'mkdir': 'MKDIR',
        'pwd': 'PWD',
        'cat': 'CAT',
        
        # IA
        'ia': 'IA',
        'ask': 'ASK',
        'summarize': 'SUMMARIZE',
        'codeexplain': 'CODEEXPLAIN',
        'translate': 'TRANSLATE',
        
        # Controle
        'history': 'HISTORY',
        'clear': 'CLEAR',
        'help': 'HELP',
        'exit': 'EXIT',
    }

    # Caracteres ignorados (espaços e tabs)
    t_ignore = ' \t'

    # Símbolos simples
    t_SLASH = r'/'

    def __init__(self):
        """Inicializa o lexer."""
        self.lexer: Optional[lex.Lexer] = None
        self.build()

    def build(self, **kwargs):
        """
        Constrói o lexer.
        """
        self.lexer = lex.lex(module=self, **kwargs)

    def t_LONG_OPTION(self, t):
        r'--[a-zA-Z][a-zA-Z0-9_-]+'
        # Remove os dois hífens do início
        t.value = t.value[2:]
        return t

    def t_OPTION_SHORT(self, t):
        r'-[a-zA-Z]+'
        # Remove o hífen do início
        t.value = t.value[1:]
        return t

    def t_STRING(self, t):
        r'"([^"\\]|\\.)*"'
        # Remove as aspas e processa escapes
        t.value = t.value[1:-1]  # Remove aspas
        t.value = t.value.replace('\\"', '"')  # Processa escape de aspas
        t.value = t.value.replace('\\n', '\n')  # Processa escape de nova linha
        t.value = t.value.replace('\\t', '\t')  # Processa escape de tab
        return t

    def t_NUMBER(self, t):
        r'\d+'
        t.value = int(t.value)
        return t

    def t_DOTDOT(self, t):
        r'\.\.'
        return t

    def t_DOT(self, t):
        r'\.'
        return t

    def t_TILDE(self, t):
        r'~'
        return t

    # PATH deve vir antes de IDENTIFIER
    def t_PATH(self, t):
        r'(/[a-zA-Z0-9_./~-]+|~/[a-zA-Z0-9_./~-]+|\./[a-zA-Z0-9_./~-]+|\.\./[a-zA-Z0-9_./~-]+|[a-zA-Z0-9_-]+/[a-zA-Z0-9_./~-]*)'
        # Reconhece:
        # /path - absoluto
        # ~/path - home
        # ./path - relativo atual
        # ../path - relativo pai
        # dir/path - relativo com dir
        return t

    def t_IDENTIFIER(self, t):
        r'[a-zA-Z_][a-zA-Z0-9_.-]*'
        # Verifica se é uma palavra reservada
        t.type = self.reserved.get(t.value, 'IDENTIFIER')
        return t

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)
        # Não retorna token, apenas incrementa linha

    def t_COMMENT(self, t):
        r'\#.*'
        pass  # Ignora comentários

    def t_error(self, t):
        """
        Tratamento de erro para caracteres inválidos.
        """
        print(f"Caractere ilegal '{t.value[0]}' na linha {t.lineno}")
        t.lexer.skip(1)

    def tokenize(self, data: str):
        """
        Tokeniza uma string de entrada.
        
        Args:
            data: String contendo o comando a ser tokenizado
            
        Yields:
            Tokens encontrados na entrada
        """
        self.lexer.input(data)
        while True:
            tok = self.lexer.token()
            if not tok:
                break
            yield tok

    def tokenize_to_list(self, data: str) -> list:
        """
        Tokeniza uma string e retorna lista de tokens.
        
        Args:
            data: String contendo o comando a ser tokenizado
            
        Returns:
            Lista de tokens
        """
        return list(self.tokenize(data))

    def print_tokens(self, data: str):
        """
        Tokeniza e imprime tokens de forma formatada (útil para debug).
        
        Args:
            data: String contendo o comando a ser tokenizado
        """
        print(f"\nTokenizando: '{data}'")
        print("-" * 50)
        self.lexer.input(data)
        while True:
            tok = self.lexer.token()
            if not tok:
                break
            print(f"Token: {tok.type:15s} | Valor: {tok.value}")
        print("-" * 50)


def main():
    """
    Função principal para testes do lexer.
    """
    lexer = TermIALexer()
    
    # Testes básicos
    test_cases = [
        'ls -la /home/user',
        'cd ..',
        'mkdir -p projects/2024',
        'cat README.md',
        'pwd',
        'ia ask "Qual é a capital da França?"',
        'ia summarize "Lorem ipsum dolor sit amet" --length medium',
        'ia codeexplain main.py',
        'ia translate "Hello World" --to pt',
        'history 10',
        'clear',
        'help ls',
        'exit',
    ]
    
    print("=" * 60)
    print("TESTE DO LEXER - TermIA")
    print("=" * 60)
    
    for test in test_cases:
        lexer.print_tokens(test)
        print()


if __name__ == '__main__':
    main()