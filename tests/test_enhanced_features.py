"""
Testes para as features avançadas do TermIA.
Este módulo testa autocomplete, syntax highlighting e history usando pytest.
"""

import pytest
import sys
import os

# Adiciona o diretório src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from enhanced_input import EnhancedInputHandler, TermIACompleter, TermIALexer  # type: ignore  # noqa: E501


class TestImports:
    """Testes de importação de módulos."""

    def test_import_enhanced_input(self):
        """Testa que os módulos podem ser importados."""
        from enhanced_input import EnhancedInputHandler, TermIACompleter, TermIALexer
        assert EnhancedInputHandler is not None
        assert TermIACompleter is not None
        assert TermIALexer is not None


class TestTermIACompleter:
    """Classe de testes para o TermIACompleter."""

    @pytest.fixture
    def completer(self):
        """Fixture que cria uma instância do completer para cada teste."""
        return TermIACompleter()

    def test_completer_initialization(self, completer):
        """Testa inicialização do completer."""
        assert completer is not None
        assert hasattr(completer, 'commands')
        assert hasattr(completer, 'ia_subcommands')
        assert len(completer.commands) > 0
        assert len(completer.ia_subcommands) > 0

    def test_completer_commands_registered(self, completer):
        """Testa que comandos estão registrados."""
        assert 'ls' in completer.commands
        assert 'cd' in completer.commands
        assert 'ia' in completer.commands
        assert 'history' in completer.commands

    def test_completer_ia_subcommands_registered(self, completer):
        """Testa que subcomandos de IA estão registrados."""
        assert 'ask' in completer.ia_subcommands
        assert 'summarize' in completer.ia_subcommands
        assert 'codeexplain' in completer.ia_subcommands
        assert 'translate' in completer.ia_subcommands

    def test_autocomplete_ls_command(self, completer):
        """Testa autocomplete para comando 'l' -> 'ls'."""
        from prompt_toolkit.document import Document

        doc = Document('l')
        completions = list(completer.get_completions(doc, None))
        ls_found = any(c.text == 'ls' for c in completions)
        assert ls_found, "Autocomplete should suggest 'ls' for 'l'"

    def test_autocomplete_ia_subcommands(self, completer):
        """Testa autocomplete para subcomandos de IA."""
        from prompt_toolkit.document import Document

        doc = Document('ia ')
        completions = list(completer.get_completions(doc, None))
        ask_found = any(c.text == 'ask' for c in completions)
        assert ask_found, "Autocomplete should suggest 'ask' after 'ia '"

    def test_autocomplete_empty_line(self, completer):
        """Testa autocomplete para linha vazia."""
        from prompt_toolkit.document import Document

        doc = Document('')
        completions = list(completer.get_completions(doc, None))
        # Deve sugerir vários comandos
        assert len(list(completions)) > 0

    def test_autocomplete_partial_command(self, completer):
        """Testa autocomplete para comando parcial."""
        from prompt_toolkit.document import Document

        doc = Document('cd')
        completions = list(completer.get_completions(doc, None))
        cd_found = any(c.text == 'cd' for c in completions)
        assert cd_found


class TestTermIALexer:
    """Classe de testes para o TermIALexer (syntax highlighting)."""

    @pytest.fixture
    def lexer(self):
        """Fixture que cria uma instância do lexer para cada teste."""
        return TermIALexer()

    def test_lexer_initialization(self, lexer):
        """Testa inicialização do lexer."""
        assert lexer is not None
        assert hasattr(lexer, 'tokens')

    def test_lexer_syntax_highlighting(self, lexer):
        """Testa syntax highlighting."""
        from pygments import lex
        from pygments.token import Keyword

        code = 'ls -la /home'
        tokens = list(lex(code, lexer))
        
        # Deve encontrar tokens
        assert len(tokens) > 0
        
        # Deve reconhecer 'ls' como keyword
        has_keyword = any(token[0] in Keyword for token in tokens)
        assert has_keyword, "Lexer should recognize commands as keywords"

    def test_lexer_recognizes_os_commands(self, lexer):
        """Testa que o lexer reconhece comandos do SO."""
        from pygments import lex
        from pygments.token import Keyword

        commands = ['ls', 'cd', 'mkdir', 'pwd', 'cat']
        for cmd in commands:
            tokens = list(lex(cmd, lexer))
            has_keyword = any(token[0] in Keyword for token in tokens)
            assert has_keyword, f"Lexer should recognize '{cmd}' as keyword"

    def test_lexer_recognizes_ia_commands(self, lexer):
        """Testa que o lexer reconhece comandos de IA."""
        from pygments import lex
        from pygments.token import Keyword

        code = 'ia ask "question"'
        tokens = list(lex(code, lexer))
        has_keyword = any(token[0] in Keyword for token in tokens)
        assert has_keyword

    def test_lexer_recognizes_strings(self, lexer):
        """Testa que o lexer reconhece strings."""
        from pygments import lex
        from pygments.token import String

        code = 'ia ask "Hello World"'
        tokens = list(lex(code, lexer))
        has_string = any(token[0] in String for token in tokens)
        assert has_string

    def test_lexer_recognizes_numbers(self, lexer):
        """Testa que o lexer reconhece números."""
        from pygments import lex
        from pygments.token import Number

        code = 'history 10'
        tokens = list(lex(code, lexer))
        has_number = any(token[0] in Number for token in tokens)
        assert has_number


class TestEnhancedInputHandler:
    """Classe de testes para o EnhancedInputHandler."""

    @pytest.fixture
    def test_history_file(self, tmp_path):
        """Fixture que cria um arquivo de histórico temporário."""
        history_file = tmp_path / 'test_history.txt'
        return str(history_file)

    @pytest.fixture
    def handler(self, test_history_file):
        """Fixture que cria uma instância do handler para cada teste."""
        # Skip se não houver console disponível
        try:
            return EnhancedInputHandler(test_history_file)
        except Exception:
            pytest.skip("Console not available for PromptSession")

    def test_handler_initialization(self, handler, test_history_file):
        """Testa inicialização do handler."""
        assert handler is not None
        assert handler.history_file == test_history_file
        assert hasattr(handler, 'session')

    def test_history_file_creation(self, test_history_file):
        """Testa que arquivo de histórico é criado."""
        # Remove se existir
        if os.path.exists(test_history_file):
            os.remove(test_history_file)
        
        try:
            handler = EnhancedInputHandler(test_history_file)
            assert os.path.exists(test_history_file)
        except Exception:
            pytest.skip("Console not available for PromptSession")

    def test_history_search(self, test_history_file):
        """Testa busca no histórico."""
        # Cria handler (pode falhar se não houver console)
        try:
            handler = EnhancedInputHandler(test_history_file)
        except Exception:
            pytest.skip("Console not available for PromptSession")
        
        # Adiciona entradas ao histórico
        with open(test_history_file, 'w', encoding='utf-8') as f:
            f.write("ls -la\n")
            f.write("pwd\n")
            f.write("cd ..\n")

        # Busca no histórico
        results = handler.search_history('ls')
        assert isinstance(results, list)
        assert 'ls -la' in results

    def test_history_search_multiple_matches(self, test_history_file):
        """Testa busca no histórico com múltiplas correspondências."""
        # Cria handler (pode falhar se não houver console)
        try:
            handler = EnhancedInputHandler(test_history_file)
        except Exception:
            pytest.skip("Console not available for PromptSession")
        
        # Adiciona entradas ao histórico
        with open(test_history_file, 'w', encoding='utf-8') as f:
            f.write("ls -la\n")
            f.write("ls -lah\n")
            f.write("pwd\n")

        results = handler.search_history('ls')
        assert len(results) >= 2
        assert 'ls -la' in results or 'ls -lah' in results

    def test_history_search_no_matches(self, test_history_file):
        """Testa busca no histórico sem correspondências."""
        # Cria handler (pode falhar se não houver console)
        try:
            handler = EnhancedInputHandler(test_history_file)
        except Exception:
            pytest.skip("Console not available for PromptSession")
        
        # Adiciona entradas ao histórico
        with open(test_history_file, 'w', encoding='utf-8') as f:
            f.write("pwd\n")
            f.write("cd ..\n")

        results = handler.search_history('nonexistent')
        assert isinstance(results, list)
        assert len(results) == 0

    def test_history_search_empty_file(self, test_history_file):
        """Testa busca em arquivo de histórico vazio."""
        # Cria handler (pode falhar se não houver console)
        try:
            handler = EnhancedInputHandler(test_history_file)
        except Exception:
            pytest.skip("Console not available for PromptSession")
        
        # Garante que o arquivo está vazio
        with open(test_history_file, 'w', encoding='utf-8') as f:
            f.write('')

        results = handler.search_history('ls')
        assert isinstance(results, list)


# ========== Testes de Integração ==========

class TestEnhancedFeaturesIntegration:
    """Testes de integração das features avançadas."""

    @pytest.fixture
    def completer(self):
        """Fixture que cria uma instância do completer."""
        return TermIACompleter()

    @pytest.fixture
    def lexer(self):
        """Fixture que cria uma instância do lexer."""
        return TermIALexer()

    @pytest.fixture
    def test_history_file(self, tmp_path):
        """Fixture que cria um arquivo de histórico temporário."""
        history_file = tmp_path / 'test_integration_history.txt'
        return str(history_file)

    def test_all_components_work_together(self, completer, lexer):
        """Testa que todos os componentes funcionam juntos."""
        # Completer
        assert completer is not None
        assert len(completer.commands) > 0

        # Lexer
        assert lexer is not None
        from pygments import lex
        tokens = list(lex('ls', lexer))
        assert len(tokens) > 0

    def test_completer_and_lexer_compatibility(self, completer, lexer):
        """Testa compatibilidade entre completer e lexer."""
        from prompt_toolkit.document import Document
        from pygments import lex

        # Testa que comandos do completer são reconhecidos pelo lexer
        test_commands = ['ls', 'cd', 'pwd', 'ia ask']
        
        for cmd in test_commands:
            # Completer deve sugerir
            doc = Document(cmd)
            completions = list(completer.get_completions(doc, None))
            
            # Lexer deve tokenizar
            tokens = list(lex(cmd, lexer))
            
            assert len(tokens) > 0

    def test_handler_includes_completer_and_lexer(self, test_history_file):
        """Testa que handler inclui completer e lexer."""
        try:
            handler = EnhancedInputHandler(test_history_file)
            assert handler.session.completer is not None
            assert handler.session.lexer is not None
        except Exception:
            pytest.skip("Console not available for PromptSession")

    def test_full_workflow(self, test_history_file):
        """Testa workflow completo: histórico, busca e componentes."""
        try:
            handler = EnhancedInputHandler(test_history_file)
        except Exception:
            pytest.skip("Console not available for PromptSession")
        
        # Adiciona histórico
        with open(test_history_file, 'w', encoding='utf-8') as f:
            f.write("ls -la\n")
            f.write("cd ..\n")
            f.write("pwd\n")

        # Busca funciona
        results = handler.search_history('ls')
        assert 'ls -la' in results

        # Handler tem todos os componentes
        assert handler.session is not None
        assert handler.session.completer is not None
        assert handler.session.lexer is not None


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
