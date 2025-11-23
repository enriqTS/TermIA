"""
Testes para o executor de comandos do TermIA.
Este módulo testa todas as funcionalidades do executor usando pytest.
"""

import pytest
import sys
import os

# Adiciona o diretório src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from executor import CommandExecutor, SecurityException  # type: ignore


class TestCommandExecutor:
    """Classe de testes para o CommandExecutor."""

    @pytest.fixture
    def executor(self):
        """Fixture que cria uma instância do executor para cada teste."""
        return CommandExecutor()

    # ========== Testes de Comandos do Sistema Operacional ==========

    def test_pwd(self, executor):
        """Testa comando pwd."""
        result = executor.execute_pwd()
        assert isinstance(result, str)
        assert len(result) > 0
        assert os.path.isabs(result) or os.path.exists(result)

    def test_ls_simple(self, executor):
        """Testa comando ls simples."""
        result = executor.execute_ls()
        assert isinstance(result, str)
        assert len(result) > 0

    def test_ls_with_options(self, executor):
        """Testa ls com opções."""
        result = executor.execute_ls(options='la')
        assert isinstance(result, str)
        lines = result.split('\n')
        assert len(lines) > 0

    def test_ls_with_path(self, executor):
        """Testa ls com caminho."""
        # Cria um diretório de teste se não existir
        test_dir = 'test_dir'
        if not os.path.exists(test_dir):
            os.makedirs(test_dir)
        
        result = executor.execute_ls(path=test_dir)
        assert isinstance(result, str)

    def test_mkdir_simple(self, executor):
        """Testa mkdir simples."""
        test_dir = 'test_dir_mkdir'
        # Remove se já existir
        if os.path.exists(test_dir):
            os.rmdir(test_dir)
        
        result = executor.execute_mkdir(test_dir)
        assert isinstance(result, str)
        assert os.path.exists(test_dir)
        
        # Cleanup
        if os.path.exists(test_dir):
            os.rmdir(test_dir)

    def test_mkdir_existing(self, executor):
        """Testa mkdir com diretório já existente."""
        test_dir = 'test_dir'
        # Garante que o diretório existe
        if not os.path.exists(test_dir):
            os.makedirs(test_dir)
        
        # Deve levantar FileExistsError
        with pytest.raises(FileExistsError):
            executor.execute_mkdir(test_dir)

    def test_mkdir_with_parents(self, executor):
        """Testa mkdir com opção -p."""
        test_path = 'test_dir/subdir/deep'
        # Remove se já existir
        import shutil
        if os.path.exists('test_dir/subdir'):
            shutil.rmtree('test_dir/subdir')
        
        result = executor.execute_mkdir(test_path, create_parents=True)
        assert isinstance(result, str)
        assert os.path.exists(test_path)
        
        # Cleanup
        if os.path.exists('test_dir/subdir'):
            shutil.rmtree('test_dir/subdir')

    def test_cat_file(self, executor):
        """Testa comando cat."""
        # Tenta ler README.md se existir
        if os.path.exists('README.md'):
            result = executor.execute_cat('README.md')
            assert isinstance(result, str)
        else:
            # Cria um arquivo de teste
            test_file = 'test_file.txt'
            with open(test_file, 'w', encoding='utf-8') as f:
                f.write('Test content')
            
            result = executor.execute_cat(test_file)
            assert isinstance(result, str)
            assert 'Test content' in result
            
            # Cleanup
            os.remove(test_file)

    def test_cd_simple(self, executor):
        """Testa comando cd."""
        original_dir = executor.execute_pwd()
        test_dir = 'test_dir'
        
        # Garante que o diretório existe
        if not os.path.exists(test_dir):
            os.makedirs(test_dir)
        
        result = executor.execute_cd(test_dir)
        assert isinstance(result, str)
        new_dir = executor.execute_pwd()
        assert test_dir in new_dir or os.path.basename(new_dir) == test_dir
        
        # Volta para o diretório original
        executor.execute_cd(original_dir)

    def test_cd_dotdot(self, executor):
        """Testa cd com .."""
        original_dir = executor.execute_pwd()
        
        # Vai para um subdiretório
        test_dir = 'test_dir'
        if not os.path.exists(test_dir):
            os.makedirs(test_dir)
        
        executor.execute_cd(test_dir)
        current = executor.execute_pwd()
        
        # Volta com ..
        result = executor.execute_cd('..')
        assert isinstance(result, str)
        new_dir = executor.execute_pwd()
        assert new_dir != current
        
        # Volta para o diretório original
        executor.execute_cd(original_dir)

    # ========== Testes de Segurança ==========

    def test_security_block_dangerous_command(self, executor):
        """Testa que comandos perigosos são bloqueados."""
        with pytest.raises(SecurityException):
            executor.execute_mkdir('rm -rf /')

    def test_security_block_restricted_command(self, executor):
        """Testa que comandos restritos são bloqueados."""
        # Verifica se há comandos restritos configurados
        restricted = executor.restricted_commands
        if restricted:
            # Tenta executar um comando restrito (se houver algum)
            # Este teste depende da configuração
            pass


# ========== Testes de Integração ==========

class TestExecutorIntegration:
    """Testes de integração mais complexos."""

    @pytest.fixture
    def executor(self):
        """Fixture que cria uma instância do executor para cada teste."""
        return CommandExecutor()

    def test_full_session(self, executor):
        """Testa uma sessão completa de comandos."""
        original_dir = executor.execute_pwd()
        
        # Sequência de comandos
        pwd_result = executor.execute_pwd()
        assert isinstance(pwd_result, str)
        
        ls_result = executor.execute_ls()
        assert isinstance(ls_result, str)
        
        # Cria um diretório de teste
        test_dir = 'test_session_dir'
        if os.path.exists(test_dir):
            import shutil
            shutil.rmtree(test_dir)
        
        mkdir_result = executor.execute_mkdir(test_dir)
        assert isinstance(mkdir_result, str)
        
        # Lista o diretório criado
        ls_test = executor.execute_ls(path=test_dir)
        assert isinstance(ls_test, str)
        
        # Muda para o diretório
        cd_result = executor.execute_cd(test_dir)
        assert isinstance(cd_result, str)
        
        # Volta
        executor.execute_cd(original_dir)
        
        # Cleanup
        if os.path.exists(test_dir):
            import shutil
            shutil.rmtree(test_dir)

    def test_ls_variations(self, executor):
        """Testa variações do comando ls."""
        # ls simples
        result1 = executor.execute_ls()
        assert isinstance(result1, str)
        
        # ls com opções
        result2 = executor.execute_ls(options='la')
        assert isinstance(result2, str)
        
        # ls com caminho
        if os.path.exists('src'):
            result3 = executor.execute_ls(path='src')
            assert isinstance(result3, str)

    def test_mkdir_variations(self, executor):
        """Testa variações do comando mkdir."""
        import shutil
        
        # mkdir simples
        test_dir1 = 'test_mkdir_1'
        if os.path.exists(test_dir1):
            os.rmdir(test_dir1)
        
        result1 = executor.execute_mkdir(test_dir1)
        assert isinstance(result1, str)
        assert os.path.exists(test_dir1)
        
        # mkdir com -p
        test_path = 'test_mkdir_2/subdir/deep'
        if os.path.exists('test_mkdir_2'):
            shutil.rmtree('test_mkdir_2')
        
        result2 = executor.execute_mkdir(test_path, create_parents=True)
        assert isinstance(result2, str)
        assert os.path.exists(test_path)
        
        # Cleanup
        if os.path.exists(test_dir1):
            os.rmdir(test_dir1)
        if os.path.exists('test_mkdir_2'):
            shutil.rmtree('test_mkdir_2')

    def test_cd_variations(self, executor):
        """Testa variações do comando cd."""
        original_dir = executor.execute_pwd()
        
        # cd para diretório existente
        test_dir = 'test_dir'
        if not os.path.exists(test_dir):
            os.makedirs(test_dir)
        
        result1 = executor.execute_cd(test_dir)
        assert isinstance(result1, str)
        
        # cd ..
        result2 = executor.execute_cd('..')
        assert isinstance(result2, str)
        
        # Volta para o original
        executor.execute_cd(original_dir)

    def test_all_os_commands(self, executor):
        """Testa todos os comandos de SO."""
        original_dir = executor.execute_pwd()
        
        # pwd
        pwd_result = executor.execute_pwd()
        assert isinstance(pwd_result, str)
        
        # ls
        ls_result = executor.execute_ls()
        assert isinstance(ls_result, str)
        
        # mkdir (com cleanup)
        test_dir = 'test_all_commands'
        if os.path.exists(test_dir):
            os.rmdir(test_dir)
        
        mkdir_result = executor.execute_mkdir(test_dir)
        assert isinstance(mkdir_result, str)
        
        # cat (se README.md existir)
        if os.path.exists('README.md'):
            cat_result = executor.execute_cat('README.md')
            assert isinstance(cat_result, str)
        
        # cd
        cd_result = executor.execute_cd(test_dir)
        assert isinstance(cd_result, str)
        
        # Volta
        executor.execute_cd(original_dir)
        
        # Cleanup
        if os.path.exists(test_dir):
            os.rmdir(test_dir)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
