"""
Testes para o analisador sintático do TermIA.
Este módulo testa todas as funcionalidades do parser usando pytest.

Autor: [Seu Nome]
Data: Outubro 2024
"""

import pytest
import sys
import os

# Adiciona o diretório src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from parser import TermIAParser
from ast_nodes import (
    LSCommand, CDCommand, MkdirCommand, PwdCommand, CatCommand,
    IAAskCommand, IASummarizeCommand, IACodeExplainCommand, IATranslateCommand,
    HistoryCommand, ClearCommand, HelpCommand, ExitCommand
)


class TestTermIAParser:
    """Classe de testes para o TermIAParser."""

    @pytest.fixture
    def parser(self):
        """Fixture que cria uma instância do parser para cada teste."""
        return TermIAParser()

    # ========== Testes de Comandos do Sistema Operacional ==========

    def test_ls_simple(self, parser):
        """Testa parsing do comando ls simples."""
        ast = parser.parse("ls")
        assert isinstance(ast, LSCommand)
        assert ast.options is None
        assert ast.path == '.'

    def test_ls_with_options(self, parser):
        """Testa ls com opções."""
        ast = parser.parse("ls -la")
        assert isinstance(ast, LSCommand)
        assert ast.options == 'la'
        assert ast.path == '.'

    def test_ls_with_path(self, parser):
        """Testa ls com caminho."""
        ast = parser.parse("ls /home/user")
        assert isinstance(ast, LSCommand)
        assert ast.options is None
        assert ast.path == '/home/user'

    def test_ls_with_options_and_path(self, parser):
        """Testa ls com opções e caminho."""
        ast = parser.parse("ls -lah /var/log")
        assert isinstance(ast, LSCommand)
        assert ast.options == 'lah'
        assert ast.path == '/var/log'

    def test_cd_with_path(self, parser):
        """Testa cd com caminho."""
        ast = parser.parse("cd /home/user")
        assert isinstance(ast, CDCommand)
        assert ast.path == '/home/user'

    def test_cd_simple(self, parser):
        """Testa cd sem argumentos."""
        ast = parser.parse("cd")
        assert isinstance(ast, CDCommand)
        assert ast.path == '~'

    def test_cd_dotdot(self, parser):
        """Testa cd com .."""
        ast = parser.parse("cd ..")
        assert isinstance(ast, CDCommand)
        assert ast.path == '..'

    def test_cd_tilde(self, parser):
        """Testa cd com ~."""
        ast = parser.parse("cd ~")
        assert isinstance(ast, CDCommand)
        assert ast.path == '~'

    def test_mkdir_simple(self, parser):
        """Testa mkdir simples."""
        ast = parser.parse("mkdir test")
        assert isinstance(ast, MkdirCommand)
        assert ast.path == 'test'
        assert ast.create_parents is False

    def test_mkdir_with_p(self, parser):
        """Testa mkdir com opção -p."""
        ast = parser.parse("mkdir -p projects/2024")
        assert isinstance(ast, MkdirCommand)
        assert ast.path == 'projects/2024'
        assert ast.create_parents is True

    def test_pwd(self, parser):
        """Testa comando pwd."""
        ast = parser.parse("pwd")
        assert isinstance(ast, PwdCommand)

    def test_cat(self, parser):
        """Testa comando cat."""
        ast = parser.parse("cat README.md")
        assert isinstance(ast, CatCommand)
        assert ast.filepath == 'README.md'

    def test_cat_with_path(self, parser):
        """Testa cat com caminho."""
        ast = parser.parse("cat /etc/hosts")
        assert isinstance(ast, CatCommand)
        assert ast.filepath == '/etc/hosts'

    # ========== Testes de Comandos de IA ==========

    def test_ia_ask(self, parser):
        """Testa comando ia ask."""
        ast = parser.parse('ia ask "O que é Python?"')
        assert isinstance(ast, IAAskCommand)
        assert ast.question == "O que é Python?"

    def test_ia_ask_long(self, parser):
        """Testa ia ask com pergunta longa."""
        question = "Como implementar um compilador usando Python e PLY?"
        ast = parser.parse(f'ia ask "{question}"')
        assert isinstance(ast, IAAskCommand)
        assert ast.question == question

    def test_ia_summarize_simple(self, parser):
        """Testa ia summarize simples."""
        text = "Lorem ipsum dolor sit amet"
        ast = parser.parse(f'ia summarize "{text}"')
        assert isinstance(ast, IASummarizeCommand)
        assert ast.text == text
        assert ast.length == 'short'

    def test_ia_summarize_with_length(self, parser):
        """Testa ia summarize com opção de tamanho."""
        text = "Texto para resumir"
        ast = parser.parse(f'ia summarize "{text}" --length medium')
        assert isinstance(ast, IASummarizeCommand)
        assert ast.text == text
        assert ast.length == 'medium'

    def test_ia_summarize_long(self, parser):
        """Testa ia summarize com length long."""
        text = "Texto longo aqui"
        ast = parser.parse(f'ia summarize "{text}" --length long')
        assert isinstance(ast, IASummarizeCommand)
        assert ast.length == 'long'

    def test_ia_codeexplain(self, parser):
        """Testa ia codeexplain."""
        ast = parser.parse("ia codeexplain main.py")
        assert isinstance(ast, IACodeExplainCommand)
        assert ast.filepath == 'main.py'

    def test_ia_codeexplain_with_path(self, parser):
        """Testa ia codeexplain com caminho."""
        ast = parser.parse("ia codeexplain src/lexer.py")
        assert isinstance(ast, IACodeExplainCommand)
        assert ast.filepath == 'src/lexer.py'

    def test_ia_translate(self, parser):
        """Testa ia translate."""
        ast = parser.parse('ia translate "Hello World" --to pt')
        assert isinstance(ast, IATranslateCommand)
        assert ast.text == "Hello World"
        assert ast.target_language == 'pt'

    def test_ia_translate_to_spanish(self, parser):
        """Testa ia translate para espanhol."""
        ast = parser.parse('ia translate "Good morning" --to es')
        assert isinstance(ast, IATranslateCommand)
        assert ast.target_language == 'es'

    # ========== Testes de Comandos de Controle ==========

    def test_history_simple(self, parser):
        """Testa comando history simples."""
        ast = parser.parse("history")
        assert isinstance(ast, HistoryCommand)
        assert ast.count == 10

    def test_history_with_count(self, parser):
        """Testa history com número."""
        ast = parser.parse("history 20")
        assert isinstance(ast, HistoryCommand)
        assert ast.count == 20

    def test_history_with_large_count(self, parser):
        """Testa history com número grande."""
        ast = parser.parse("history 100")
        assert isinstance(ast, HistoryCommand)
        assert ast.count == 100

    def test_clear(self, parser):
        """Testa comando clear."""
        ast = parser.parse("clear")
        assert isinstance(ast, ClearCommand)

    def test_help_simple(self, parser):
        """Testa help simples."""
        ast = parser.parse("help")
        assert isinstance(ast, HelpCommand)
        assert ast.command is None

    def test_help_with_command(self, parser):
        """Testa help com comando específico."""
        ast = parser.parse("help ls")
        assert isinstance(ast, HelpCommand)
        assert ast.command == 'ls'

    def test_help_for_ia(self, parser):
        """Testa help para comando ia."""
        ast = parser.parse("help ia")
        assert isinstance(ast, HelpCommand)
        assert ast.command == 'ia'

    def test_exit(self, parser):
        """Testa comando exit."""
        ast = parser.parse("exit")
        assert isinstance(ast, ExitCommand)

    # ========== Testes de Casos Complexos ==========

    def test_complex_ls(self, parser):
        """Testa ls complexo."""
        ast = parser.parse("ls -lah /home/user/documents")
        assert isinstance(ast, LSCommand)
        assert 'l' in ast.options
        assert 'a' in ast.options
        assert 'h' in ast.options
        assert ast.path == '/home/user/documents'

    def test_complex_mkdir(self, parser):
        """Testa mkdir complexo."""
        ast = parser.parse("mkdir -p projects/2024/termia/src")
        assert isinstance(ast, MkdirCommand)
        assert ast.create_parents is True
        assert 'projects/2024/termia/src' in ast.path

    def test_complex_ia_summarize(self, parser):
        """Testa ia summarize complexo."""
        long_text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit"
        ast = parser.parse(f'ia summarize "{long_text}" --length long')
        assert isinstance(ast, IASummarizeCommand)
        assert ast.text == long_text
        assert ast.length == 'long'

    # ========== Testes de to_dict() ==========

    def test_ls_to_dict(self, parser):
        """Testa conversão de LSCommand para dict."""
        ast = parser.parse("ls -la /home")
        d = ast.to_dict()
        assert d['type'] == 'LSCommand'
        assert d['options'] == 'la'
        assert d['path'] == '/home'

    def test_ia_ask_to_dict(self, parser):
        """Testa conversão de IAAskCommand para dict."""
        ast = parser.parse('ia ask "test"')
        d = ast.to_dict()
        assert d['type'] == 'IAAskCommand'
        assert d['question'] == 'test'

    def test_history_to_dict(self, parser):
        """Testa conversão de HistoryCommand para dict."""
        ast = parser.parse("history 15")
        d = ast.to_dict()
        assert d['type'] == 'HistoryCommand'
        assert d['count'] == 15

    # ========== Testes de Caminhos Especiais ==========

    def test_path_with_dot(self, parser):
        """Testa caminho com ponto."""
        ast = parser.parse("ls .")
        assert isinstance(ast, LSCommand)
        assert ast.path == '.'

    def test_path_with_dotdot(self, parser):
        """Testa caminho com .."""
        ast = parser.parse("cd ..")
        assert isinstance(ast, CDCommand)
        assert ast.path == '..'

    def test_path_with_tilde(self, parser):
        """Testa caminho com ~."""
        ast = parser.parse("cd ~")
        assert isinstance(ast, CDCommand)
        assert ast.path == '~'

    def test_path_relative(self, parser):
        """Testa caminho relativo."""
        ast = parser.parse("cd ./src")
        assert isinstance(ast, CDCommand)
        assert './src' in ast.path

    def test_path_absolute(self, parser):
        """Testa caminho absoluto."""
        ast = parser.parse("cd /usr/local/bin")
        assert isinstance(ast, CDCommand)
        assert ast.path == '/usr/local/bin'

    # ========== Testes de Strings Especiais ==========

    def test_string_with_spaces(self, parser):
        """Testa string com espaços."""
        ast = parser.parse('ia ask "O que é um compilador?"')
        assert isinstance(ast, IAAskCommand)
        assert ' ' in ast.question

    def test_string_with_special_chars(self, parser):
        """Testa string com caracteres especiais."""
        text = "Hello, World! How are you?"
        ast = parser.parse(f'ia ask "{text}"')
        assert isinstance(ast, IAAskCommand)
        assert ast.question == text

    def test_empty_string(self, parser):
        """Testa string vazia."""
        ast = parser.parse('ia ask ""')
        assert isinstance(ast, IAAskCommand)
        assert ast.question == ""

    # ========== Testes de Erros ==========

    def test_invalid_command(self, parser):
        """Testa comando inválido."""
        ast = parser.parse("invalid_command")
        # Parser deve retornar None ou lançar erro
        # Depende da implementação do tratamento de erro
        # Aqui apenas verificamos que não crashou

    def test_incomplete_command(self, parser):
        """Testa comando incompleto."""
        ast = parser.parse("ia")
        # Deve falhar ou retornar None


# ========== Testes de Integração ==========

class TestParserIntegration:
    """Testes de integração mais complexos."""

    @pytest.fixture
    def parser(self):
        return TermIAParser()

    def test_all_os_commands(self, parser):
        """Testa todos os comandos de SO."""
        commands = [
            ("ls", LSCommand),
            ("cd /home", CDCommand),
            ("mkdir test", MkdirCommand),
            ("pwd", PwdCommand),
            ("cat file.txt", CatCommand),
        ]
        
        for cmd, expected_type in commands:
            ast = parser.parse(cmd)
            assert isinstance(ast, expected_type), f"Falhou para: {cmd}"

    def test_all_ia_commands(self, parser):
        """Testa todos os comandos de IA."""
        commands = [
            ('ia ask "test"', IAAskCommand),
            ('ia summarize "text"', IASummarizeCommand),
            ('ia codeexplain file.py', IACodeExplainCommand),
            ('ia translate "hi" --to pt', IATranslateCommand),
        ]
        
        for cmd, expected_type in commands:
            ast = parser.parse(cmd)
            assert isinstance(ast, expected_type), f"Falhou para: {cmd}"

    def test_all_control_commands(self, parser):
        """Testa todos os comandos de controle."""
        commands = [
            ("history", HistoryCommand),
            ("clear", ClearCommand),
            ("help", HelpCommand),
            ("exit", ExitCommand),
        ]
        
        for cmd, expected_type in commands:
            ast = parser.parse(cmd)
            assert isinstance(ast, expected_type), f"Falhou para: {cmd}"

    def test_session_simulation(self, parser):
        """Simula uma sessão completa de comandos."""
        session = [
            "ls -la",
            "cd projects",
            "mkdir -p 2024/termia",
            "cd 2024/termia",
            'ia ask "O que é compilação?"',
            "pwd",
            "history 5",
            "exit"
        ]
        
        for cmd in session:
            ast = parser.parse(cmd)
            # Verifica que todos os comandos foram parseados com sucesso
            assert ast is not None, f"Falhou ao parsear: {cmd}"

    def test_repr_all_commands(self, parser):
        """Testa representação em string de todos os comandos."""
        commands = [
            "ls -la /home",
            "cd ..",
            "mkdir -p test",
            "pwd",
            "cat file.txt",
            'ia ask "test"',
            'ia summarize "text"',
            'ia codeexplain main.py',
            'ia translate "hi" --to pt',
            "history 10",
            "clear",
            "help ls",
            "exit"
        ]
        
        for cmd in commands:
            ast = parser.parse(cmd)
            # Verifica que __repr__ funciona
            repr_str = repr(ast)
            assert isinstance(repr_str, str)
            assert len(repr_str) > 0


if __name__ == '__main__':
    pytest.main([__file__, '-v'])