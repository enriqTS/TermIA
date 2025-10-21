"""
Testes para o analisador léxico do TermIA.
Este módulo testa todas as funcionalidades do lexer usando pytest.

Autor: [Seu Nome]
Data: Outubro 2024
"""

import pytest
import sys
import os

# Adiciona o diretório src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from lexer import TermIALexer


class TestTermIALexer:
    """Classe de testes para o TermIALexer."""

    @pytest.fixture
    def lexer(self):
        """Fixture que cria uma instância do lexer para cada teste."""
        return TermIALexer()

    # ========== Testes de Comandos do Sistema Operacional ==========

    def test_ls_simple(self, lexer):
        """Testa tokenização do comando ls simples."""
        tokens = lexer.tokenize_to_list("ls")
        assert len(tokens) == 1
        assert tokens[0].type == 'LS'
        assert tokens[0].value == 'ls'

    def test_ls_with_options(self, lexer):
        """Testa ls com opções."""
        tokens = lexer.tokenize_to_list("ls -la")
        assert len(tokens) == 2
        assert tokens[0].type == 'LS'
        assert tokens[1].type == 'OPTION_SHORT'
        assert tokens[1].value == 'la'

    def test_ls_with_path(self, lexer):
        """Testa ls com caminho."""
        tokens = lexer.tokenize_to_list("ls /home/user")
        assert len(tokens) == 2
        assert tokens[0].type == 'LS'
        assert tokens[1].type == 'PATH'
        assert tokens[1].value == '/home/user'

    def test_cd_command(self, lexer):
        """Testa comando cd."""
        tokens = lexer.tokenize_to_list("cd ..")
        assert len(tokens) == 2
        assert tokens[0].type == 'CD'
        assert tokens[1].type == 'DOTDOT'

    def test_mkdir_with_option(self, lexer):
        """Testa mkdir com opção -p."""
        tokens = lexer.tokenize_to_list("mkdir -p projects/2024")
        assert len(tokens) == 3
        assert tokens[0].type == 'MKDIR'
        assert tokens[1].type == 'OPTION_SHORT'
        assert tokens[1].value == 'p'
        assert tokens[2].type == 'PATH'

    def test_pwd_command(self, lexer):
        """Testa comando pwd."""
        tokens = lexer.tokenize_to_list("pwd")
        assert len(tokens) == 1
        assert tokens[0].type == 'PWD'

    def test_cat_command(self, lexer):
        """Testa comando cat."""
        tokens = lexer.tokenize_to_list("cat README.md")
        assert len(tokens) == 2
        assert tokens[0].type == 'CAT'
        assert tokens[1].type == 'IDENTIFIER'
        assert tokens[1].value == 'README.md'

    # ========== Testes de Comandos de IA ==========

    def test_ia_ask_simple(self, lexer):
        """Testa comando ia ask simples."""
        tokens = lexer.tokenize_to_list('ia ask "O que é Python?"')
        assert len(tokens) == 3
        assert tokens[0].type == 'IA'
        assert tokens[1].type == 'ASK'
        assert tokens[2].type == 'STRING'
        assert tokens[2].value == 'O que é Python?'

    def test_ia_summarize_with_option(self, lexer):
        """Testa ia summarize com opção."""
        tokens = lexer.tokenize_to_list('ia summarize "texto" --length medium')
        assert len(tokens) == 5
        assert tokens[0].type == 'IA'
        assert tokens[1].type == 'SUMMARIZE'
        assert tokens[2].type == 'STRING'
        assert tokens[3].type == 'LONG_OPTION'
        assert tokens[3].value == 'length'
        assert tokens[4].type == 'IDENTIFIER'
        assert tokens[4].value == 'medium'

    def test_ia_codeexplain(self, lexer):
        """Testa ia codeexplain."""
        tokens = lexer.tokenize_to_list("ia codeexplain main.py")
        assert len(tokens) == 3
        assert tokens[0].type == 'IA'
        assert tokens[1].type == 'CODEEXPLAIN'
        assert tokens[2].type == 'IDENTIFIER'

    def test_ia_translate(self, lexer):
        """Testa ia translate."""
        tokens = lexer.tokenize_to_list('ia translate "Hello" --to pt')
        assert len(tokens) == 5
        assert tokens[0].type == 'IA'
        assert tokens[1].type == 'TRANSLATE'
        assert tokens[2].type == 'STRING'
        assert tokens[3].type == 'LONG_OPTION'
        assert tokens[4].type == 'IDENTIFIER'

    # ========== Testes de Comandos de Controle ==========

    def test_history_command(self, lexer):
        """Testa comando history."""
        tokens = lexer.tokenize_to_list("history 10")
        assert len(tokens) == 2
        assert tokens[0].type == 'HISTORY'
        assert tokens[1].type == 'NUMBER'
        assert tokens[1].value == 10

    def test_clear_command(self, lexer):
        """Testa comando clear."""
        tokens = lexer.tokenize_to_list("clear")
        assert len(tokens) == 1
        assert tokens[0].type == 'CLEAR'

    def test_help_command(self, lexer):
        """Testa comando help."""
        tokens = lexer.tokenize_to_list("help ls")
        assert len(tokens) == 2
        assert tokens[0].type == 'HELP'
        assert tokens[1].type == 'LS'

    def test_exit_command(self, lexer):
        """Testa comando exit."""
        tokens = lexer.tokenize_to_list("exit")
        assert len(tokens) == 1
        assert tokens[0].type == 'EXIT'

    # ========== Testes de Tokens Especiais ==========

    def test_string_with_spaces(self, lexer):
        """Testa string com espaços."""
        tokens = lexer.tokenize_to_list('"Este é um texto com espaços"')
        assert len(tokens) == 1
        assert tokens[0].type == 'STRING'
        assert tokens[0].value == 'Este é um texto com espaços'

    def test_string_with_escape(self, lexer):
        """Testa string com caracteres escapados."""
        tokens = lexer.tokenize_to_list('"Texto com \\"aspas\\""')
        assert len(tokens) == 1
        assert tokens[0].type == 'STRING'
        assert tokens[0].value == 'Texto com "aspas"'

    def test_number_token(self, lexer):
        """Testa reconhecimento de números."""
        tokens = lexer.tokenize_to_list("history 100")
        assert len(tokens) == 2
        assert tokens[1].type == 'NUMBER'
        assert tokens[1].value == 100

    def test_path_absolute(self, lexer):
        """Testa caminho absoluto."""
        tokens = lexer.tokenize_to_list("cd /home/user/documents")
        assert len(tokens) == 2
        assert tokens[1].type == 'PATH'
        assert tokens[1].value == '/home/user/documents'

    def test_path_relative(self, lexer):
        """Testa caminho relativo."""
        tokens = lexer.tokenize_to_list("cd ./src")
        assert len(tokens) == 2
        assert tokens[1].type == 'PATH'

    def test_path_home(self, lexer):
        """Testa caminho com til (~)."""
        tokens = lexer.tokenize_to_list("cd ~/projects")
        assert len(tokens) == 2
        assert tokens[1].type == 'PATH'

    def test_dot_token(self, lexer):
        """Testa token ponto (.)."""
        tokens = lexer.tokenize_to_list("cd .")
        assert len(tokens) == 2
        assert tokens[1].type == 'DOT'

    def test_dotdot_token(self, lexer):
        """Testa token dois pontos (..)."""
        tokens = lexer.tokenize_to_list("cd ..")
        assert len(tokens) == 2
        assert tokens[1].type == 'DOTDOT'

    def test_tilde_token(self, lexer):
        """Testa token til (~)."""
        tokens = lexer.tokenize_to_list("cd ~")
        assert len(tokens) == 2
        assert tokens[1].type == 'TILDE'

    # ========== Testes de Opções ==========

    def test_short_option_single(self, lexer):
        """Testa opção curta única."""
        tokens = lexer.tokenize_to_list("ls -a")
        assert len(tokens) == 2
        assert tokens[1].type == 'OPTION_SHORT'
        assert tokens[1].value == 'a'

    def test_short_option_combined(self, lexer):
        """Testa opções curtas combinadas."""
        tokens = lexer.tokenize_to_list("ls -lah")
        assert len(tokens) == 2
        assert tokens[1].type == 'OPTION_SHORT'
        assert tokens[1].value == 'lah'

    def test_long_option(self, lexer):
        """Testa opção longa."""
        tokens = lexer.tokenize_to_list("ia summarize text --length short")
        tokens_filtered = [t for t in tokens if t.type == 'LONG_OPTION']
        assert len(tokens_filtered) == 1
        assert tokens_filtered[0].value == 'length'

    # ========== Testes de Casos Complexos ==========

    def test_complex_command_1(self, lexer):
        """Testa comando complexo: ls com múltiplas opções e caminho."""
        tokens = lexer.tokenize_to_list("ls -lah /home/user/documents")
        assert len(tokens) == 3
        assert tokens[0].type == 'LS'
        assert tokens[1].type == 'OPTION_SHORT'
        assert tokens[2].type == 'PATH'

    def test_complex_command_2(self, lexer):
        """Testa comando complexo: ia com string longa."""
        cmd = 'ia ask "Como implementar um lexer em Python usando PLY?"'
        tokens = lexer.tokenize_to_list(cmd)
        assert len(tokens) == 3
        assert tokens[0].type == 'IA'
        assert tokens[1].type == 'ASK'
        assert tokens[2].type == 'STRING'

    def test_multiple_spaces(self, lexer):
        """Testa comando com múltiplos espaços."""
        tokens = lexer.tokenize_to_list("ls    -l    /home")
        assert len(tokens) == 3
        assert tokens[0].type == 'LS'
        assert tokens[1].type == 'OPTION_SHORT'
        assert tokens[2].type == 'PATH'

    # ========== Testes de Identificadores ==========

    def test_identifier_simple(self, lexer):
        """Testa identificador simples."""
        tokens = lexer.tokenize_to_list("cat file.txt")
        assert len(tokens) == 2
        assert tokens[1].type == 'IDENTIFIER'
        assert tokens[1].value == 'file.txt'

    def test_identifier_with_underscore(self, lexer):
        """Testa identificador com underscore."""
        tokens = lexer.tokenize_to_list("cat my_file.txt")
        assert len(tokens) == 2
        assert tokens[1].type == 'IDENTIFIER'
        assert tokens[1].value == 'my_file.txt'

    def test_identifier_with_dash(self, lexer):
        """Testa identificador com hífen."""
        tokens = lexer.tokenize_to_list("cat my-file.txt")
        assert len(tokens) == 2
        assert tokens[1].type == 'IDENTIFIER'

    # ========== Testes de Comentários ==========

    def test_comment_ignored(self, lexer):
        """Testa que comentários são ignorados."""
        tokens = lexer.tokenize_to_list("ls # isso é um comentário")
        assert len(tokens) == 1
        assert tokens[0].type == 'LS'

    # ========== Testes de Casos Edge ==========

    def test_empty_string(self, lexer):
        """Testa string vazia."""
        tokens = lexer.tokenize_to_list("")
        assert len(tokens) == 0

    def test_only_spaces(self, lexer):
        """Testa entrada apenas com espaços."""
        tokens = lexer.tokenize_to_list("   ")
        assert len(tokens) == 0

    def test_reserved_word_as_identifier(self, lexer):
        """Testa que palavras reservadas são reconhecidas corretamente."""
        tokens = lexer.tokenize_to_list("ls")
        assert tokens[0].type == 'LS'
        # Não deve ser IDENTIFIER


# ========== Testes de Integração ==========

class TestLexerIntegration:
    """Testes de integração mais complexos."""

    @pytest.fixture
    def lexer(self):
        return TermIALexer()

    def test_full_session(self, lexer):
        """Testa uma sessão completa de comandos."""
        commands = [
            "ls -la",
            "cd projects",
            "mkdir -p 2024/termia",
            "cd 2024/termia",
            'ia ask "O que é compilação?"',
            "pwd",
            "history 5",
            "exit"
        ]
        
        for cmd in commands:
            tokens = lexer.tokenize_to_list(cmd)
            # Verifica que todos os comandos geram pelo menos 1 token
            assert len(tokens) >= 1

    def test_all_ia_commands(self, lexer):
        """Testa todos os comandos de IA."""
        ia_commands = [
            'ia ask "pergunta"',
            'ia summarize "texto" --length medium',
            'ia codeexplain file.py',
            'ia translate "text" --to pt'
        ]
        
        for cmd in ia_commands:
            tokens = lexer.tokenize_to_list(cmd)
            # Primeiro token sempre deve ser IA
            assert tokens[0].type == 'IA'

    def test_all_os_commands(self, lexer):
        """Testa todos os comandos do SO."""
        os_commands = [
            "ls -la /path",
            "cd ..",
            "mkdir -p dir",
            "pwd",
            "cat file.txt"
        ]
        
        for cmd in os_commands:
            tokens = lexer.tokenize_to_list(cmd)
            # Verifica que o comando foi reconhecido
            assert len(tokens) >= 1


if __name__ == '__main__':
    pytest.main([__file__, '-v'])