"""
Testes para o executor de comandos de IA do TermIA.
Este módulo testa todas as funcionalidades do AIExecutor usando pytest.
"""

import pytest
import sys
import os

# Adiciona o diretório src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from ai_executor import AIExecutor, AIException  # type: ignore


class TestAIExecutor:
    """Classe de testes para o AIExecutor."""

    @pytest.fixture
    def executor(self):
        """Fixture que cria uma instância do executor para cada teste."""
        return AIExecutor()

    # ========== Testes de Comandos de IA ==========

    def test_ia_ask_simple(self, executor):
        """Testa comando ia ask simples."""
        result = executor.execute_ia_ask("What is 2+2?")
        assert isinstance(result, str)
        assert len(result) > 0

    def test_ia_ask_long_question(self, executor):
        """Testa ia ask com pergunta longa."""
        question = "Como implementar um compilador usando Python e PLY?"
        result = executor.execute_ia_ask(question)
        assert isinstance(result, str)
        assert len(result) > 0

    def test_ia_summarize_short(self, executor):
        """Testa ia summarize com length short."""
        text = "Python is a high-level programming language. It was created by Guido van Rossum and first released in 1991. Python is known for its simple and readable syntax."
        result = executor.execute_ia_summarize(text, length="short")
        assert isinstance(result, str)
        assert len(result) > 0
        # Summary should typically be shorter than original
        assert len(result) < len(text) * 2  # Allow some flexibility

    def test_ia_summarize_medium(self, executor):
        """Testa ia summarize com length medium."""
        text = "Python is a high-level programming language. It was created by Guido van Rossum and first released in 1991. Python is known for its simple and readable syntax."
        result = executor.execute_ia_summarize(text, length="medium")
        assert isinstance(result, str)
        assert len(result) > 0

    def test_ia_summarize_long(self, executor):
        """Testa ia summarize com length long."""
        text = "Python is a high-level programming language. It was created by Guido van Rossum and first released in 1991. Python is known for its simple and readable syntax."
        result = executor.execute_ia_summarize(text, length="long")
        assert isinstance(result, str)
        assert len(result) > 0

    def test_ia_translate_english_to_portuguese(self, executor):
        """Testa ia translate de inglês para português."""
        result = executor.execute_ia_translate("Hello, how are you?", "pt")
        assert isinstance(result, str)
        assert len(result) > 0

    def test_ia_translate_to_spanish(self, executor):
        """Testa ia translate para espanhol."""
        result = executor.execute_ia_translate("Good morning", "es")
        assert isinstance(result, str)
        assert len(result) > 0

    def test_ia_codeexplain(self, executor):
        """Testa ia codeexplain."""
        # Cria um arquivo de teste
        test_file = "test_code_sample.py"
        try:
            with open(test_file, 'w', encoding='utf-8') as f:
                f.write('def hello():\n    print("Hello World")\n')

            result = executor.execute_ia_codeexplain(test_file)
            assert isinstance(result, str)
            assert len(result) > 0
        finally:
            # Cleanup
            if os.path.exists(test_file):
                os.remove(test_file)

    def test_ia_codeexplain_with_path(self, executor):
        """Testa ia codeexplain com caminho."""
        # Usa um arquivo existente se disponível
        test_files = ['README.md', 'main.py', 'config.yaml']
        test_file = None
        
        for file in test_files:
            if os.path.exists(file):
                test_file = file
                break
        
        if test_file:
            result = executor.execute_ia_codeexplain(test_file)
            assert isinstance(result, str)
            assert len(result) > 0

    # ========== Testes de Tratamento de Erros ==========

    def test_ia_ask_empty_question(self, executor):
        """Testa que pergunta vazia levanta AIException."""
        with pytest.raises(AIException):
            executor.execute_ia_ask("")

    def test_ia_ask_whitespace_only(self, executor):
        """Testa que pergunta apenas com espaços levanta AIException."""
        with pytest.raises(AIException):
            executor.execute_ia_ask("   ")

    def test_ia_summarize_empty_text(self, executor):
        """Testa que texto vazio levanta AIException."""
        with pytest.raises(AIException):
            executor.execute_ia_summarize("")

    def test_ia_translate_empty_text(self, executor):
        """Testa que texto vazio levanta AIException."""
        with pytest.raises(AIException):
            executor.execute_ia_translate("", "pt")

    def test_ia_codeexplain_nonexistent_file(self, executor):
        """Testa que arquivo inexistente levanta AIException."""
        with pytest.raises(AIException):
            executor.execute_ia_codeexplain("nonexistent_file_12345.py")

    def test_ia_codeexplain_empty_file(self, executor):
        """Testa que arquivo vazio levanta AIException."""
        test_file = "test_empty_file.py"
        try:
            # Cria arquivo vazio
            with open(test_file, 'w', encoding='utf-8') as f:
                f.write('')
            
            with pytest.raises(AIException):
                executor.execute_ia_codeexplain(test_file)
        finally:
            # Cleanup
            if os.path.exists(test_file):
                os.remove(test_file)


# ========== Testes de Integração ==========

class TestAIExecutorIntegration:
    """Testes de integração mais complexos."""

    @pytest.fixture
    def executor(self):
        """Fixture que cria uma instância do executor para cada teste."""
        return AIExecutor()

    def test_all_ia_commands(self, executor):
        """Testa todos os comandos de IA."""
        # ia ask
        result1 = executor.execute_ia_ask("What is Python?")
        assert isinstance(result1, str)
        assert len(result1) > 0

        # ia summarize
        text = "Python is a programming language."
        result2 = executor.execute_ia_summarize(text, length="short")
        assert isinstance(result2, str)
        assert len(result2) > 0

        # ia translate
        result3 = executor.execute_ia_translate("Hello", "pt")
        assert isinstance(result3, str)
        assert len(result3) > 0

        # ia codeexplain (se houver arquivo disponível)
        test_files = ['README.md', 'main.py']
        for test_file in test_files:
            if os.path.exists(test_file):
                result4 = executor.execute_ia_codeexplain(test_file)
                assert isinstance(result4, str)
                assert len(result4) > 0
                break

    def test_ia_summarize_all_lengths(self, executor):
        """Testa ia summarize com todos os tamanhos."""
        text = "Python is a high-level programming language. It was created by Guido van Rossum and first released in 1991. Python is known for its simple and readable syntax."
        
        for length in ["short", "medium", "long"]:
            result = executor.execute_ia_summarize(text, length=length)
            assert isinstance(result, str)
            assert len(result) > 0

    def test_ia_translate_multiple_languages(self, executor):
        """Testa ia translate para múltiplos idiomas."""
        text = "Hello"
        languages = ["pt", "es", "fr"]
        
        for lang in languages:
            result = executor.execute_ia_translate(text, lang)
            assert isinstance(result, str)
            assert len(result) > 0

    def test_ia_codeexplain_different_file_types(self, executor):
        """Testa ia codeexplain com diferentes tipos de arquivo."""
        test_files = []
        
        # Cria arquivos de teste
        try:
            # Python file
            py_file = "test_sample.py"
            with open(py_file, 'w', encoding='utf-8') as f:
                f.write('def test():\n    return True\n')
            test_files.append(py_file)
            
            # Text file
            txt_file = "test_sample.txt"
            with open(txt_file, 'w', encoding='utf-8') as f:
                f.write('This is a test file.')
            test_files.append(txt_file)
            
            # Testa cada arquivo
            for test_file in test_files:
                if os.path.exists(test_file):
                    result = executor.execute_ia_codeexplain(test_file)
                    assert isinstance(result, str)
                    assert len(result) > 0
        finally:
            # Cleanup
            for test_file in test_files:
                if os.path.exists(test_file):
                    os.remove(test_file)

    def test_session_simulation(self, executor):
        """Simula uma sessão completa de comandos de IA."""
        # Pergunta
        result1 = executor.execute_ia_ask("What is 2+2?")
        assert isinstance(result1, str)
        
        # Resumo
        text = "Python is a programming language."
        result2 = executor.execute_ia_summarize(text)
        assert isinstance(result2, str)
        
        # Tradução
        result3 = executor.execute_ia_translate("Hello World", "pt")
        assert isinstance(result3, str)
        
        # Explicação de código (se disponível)
        if os.path.exists('main.py'):
            result4 = executor.execute_ia_codeexplain('main.py')
            assert isinstance(result4, str)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
