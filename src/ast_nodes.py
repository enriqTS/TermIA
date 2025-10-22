"""
TermIA - Definição dos Nós da AST (Abstract Syntax Tree)
Este módulo define as classes que representam os nós da árvore sintática abstrata.
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Any


class ASTNode(ABC):
    """Classe base para todos os nós da AST."""
    
    @abstractmethod
    def __repr__(self) -> str:
        """Representação em string do nó."""
        pass
    
    @abstractmethod
    def to_dict(self) -> dict:
        """Converte o nó para dicionário (útil para debug)."""
        pass


# ==================== Comandos do Sistema Operacional ====================

class OSCommand(ASTNode):
    """Classe base para comandos do sistema operacional."""
    pass


class LSCommand(OSCommand):
    """Comando ls - listar arquivos."""
    
    def __init__(self, options: Optional[str] = None, path: Optional[str] = None):
        self.options = options
        self.path = path or '.'
    
    def __repr__(self) -> str:
        opts = f" -{self.options}" if self.options else ""
        return f"LSCommand({opts} {self.path})"
    
    def to_dict(self) -> dict:
        return {
            'type': 'LSCommand',
            'options': self.options,
            'path': self.path
        }


class CDCommand(OSCommand):
    """Comando cd - mudar diretório."""
    
    def __init__(self, path: Optional[str] = None):
        self.path = path or '~'
    
    def __repr__(self) -> str:
        return f"CDCommand({self.path})"
    
    def to_dict(self) -> dict:
        return {
            'type': 'CDCommand',
            'path': self.path
        }


class MkdirCommand(OSCommand):
    """Comando mkdir - criar diretório."""
    
    def __init__(self, path: str, create_parents: bool = False):
        self.path = path
        self.create_parents = create_parents
    
    def __repr__(self) -> str:
        flag = " -p" if self.create_parents else ""
        return f"MkdirCommand({flag} {self.path})"
    
    def to_dict(self) -> dict:
        return {
            'type': 'MkdirCommand',
            'path': self.path,
            'create_parents': self.create_parents
        }


class PwdCommand(OSCommand):
    """Comando pwd - mostrar diretório atual."""
    
    def __repr__(self) -> str:
        return "PwdCommand()"
    
    def to_dict(self) -> dict:
        return {'type': 'PwdCommand'}


class CatCommand(OSCommand):
    """Comando cat - exibir conteúdo de arquivo."""
    
    def __init__(self, filepath: str):
        self.filepath = filepath
    
    def __repr__(self) -> str:
        return f"CatCommand({self.filepath})"
    
    def to_dict(self) -> dict:
        return {
            'type': 'CatCommand',
            'filepath': self.filepath
        }


# ==================== Comandos de IA ====================

class IACommand(ASTNode):
    """Classe base para comandos de IA."""
    pass


class IAAskCommand(IACommand):
    """Comando ia ask - fazer pergunta."""
    
    def __init__(self, question: str):
        self.question = question
    
    def __repr__(self) -> str:
        return f"IAAskCommand('{self.question[:30]}...')"
    
    def to_dict(self) -> dict:
        return {
            'type': 'IAAskCommand',
            'question': self.question
        }


class IASummarizeCommand(IACommand):
    """Comando ia summarize - resumir texto."""
    
    def __init__(self, text: str, length: str = 'short'):
        self.text = text
        self.length = length  # short, medium, long
    
    def __repr__(self) -> str:
        return f"IASummarizeCommand(text_len={len(self.text)}, length={self.length})"
    
    def to_dict(self) -> dict:
        return {
            'type': 'IASummarizeCommand',
            'text': self.text,
            'length': self.length
        }


class IACodeExplainCommand(IACommand):
    """Comando ia codeexplain - explicar código."""
    
    def __init__(self, filepath: str):
        self.filepath = filepath
    
    def __repr__(self) -> str:
        return f"IACodeExplainCommand({self.filepath})"
    
    def to_dict(self) -> dict:
        return {
            'type': 'IACodeExplainCommand',
            'filepath': self.filepath
        }


class IATranslateCommand(IACommand):
    """Comando ia translate - traduzir texto."""
    
    def __init__(self, text: str, target_language: str):
        self.text = text
        self.target_language = target_language
    
    def __repr__(self) -> str:
        return f"IATranslateCommand(to={self.target_language})"
    
    def to_dict(self) -> dict:
        return {
            'type': 'IATranslateCommand',
            'text': self.text,
            'target_language': self.target_language
        }


# ==================== Comandos de Controle ====================

class ControlCommand(ASTNode):
    """Classe base para comandos de controle."""
    pass


class HistoryCommand(ControlCommand):
    """Comando history - mostrar histórico."""
    
    def __init__(self, count: int = 10):
        self.count = count
    
    def __repr__(self) -> str:
        return f"HistoryCommand(n={self.count})"
    
    def to_dict(self) -> dict:
        return {
            'type': 'HistoryCommand',
            'count': self.count
        }


class ClearCommand(ControlCommand):
    """Comando clear - limpar tela."""
    
    def __repr__(self) -> str:
        return "ClearCommand()"
    
    def to_dict(self) -> dict:
        return {'type': 'ClearCommand'}


class HelpCommand(ControlCommand):
    """Comando help - mostrar ajuda."""
    
    def __init__(self, command: Optional[str] = None):
        self.command = command
    
    def __repr__(self) -> str:
        cmd = f" {self.command}" if self.command else ""
        return f"HelpCommand({cmd})"
    
    def to_dict(self) -> dict:
        return {
            'type': 'HelpCommand',
            'command': self.command
        }


class ExitCommand(ControlCommand):
    """Comando exit - sair do terminal."""
    
    def __repr__(self) -> str:
        return "ExitCommand()"
    
    def to_dict(self) -> dict:
        return {'type': 'ExitCommand'}


# ==================== Utilitários ====================

def print_ast(node: ASTNode, indent: int = 0) -> None:
    """
    Imprime a AST de forma hierárquica (útil para debug).
    
    Args:
        node: Nó da AST a ser impresso
        indent: Nível de indentação
    """
    prefix = "  " * indent
    print(f"{prefix}{node}")
    
    # Se o nó tiver atributos que são listas de nós, imprime recursivamente
    if hasattr(node, '__dict__'):
        for attr_name, attr_value in node.__dict__.items():
            if isinstance(attr_value, list):
                for item in attr_value:
                    if isinstance(item, ASTNode):
                        print_ast(item, indent + 1)
            elif isinstance(attr_value, ASTNode):
                print_ast(attr_value, indent + 1)