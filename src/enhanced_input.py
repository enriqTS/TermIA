# -*- coding: utf-8 -*-
"""
TermIA - Enhanced Input Handler
This module provides autocomplete, syntax highlighting, and history features.
"""

import os
from typing import List, Iterable
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.history import FileHistory
from prompt_toolkit.lexers import PygmentsLexer
from prompt_toolkit.styles import Style
from pygments.lexer import RegexLexer, bygroups
from pygments.token import Keyword, Name, String, Number, Operator, Comment, Text


class TermIALexer(RegexLexer):
    """
    Custom Pygments lexer for TermIA syntax highlighting.
    """
    name = 'TermIA'
    aliases = ['termia']
    filenames = []

    tokens = {
        'root': [
            # OS Commands
            (r'\b(ls|cd|mkdir|pwd|cat)\b', Keyword.Reserved),
            # IA Commands
            (r'\b(ia)\b', Keyword.Namespace),
            (r'\b(ask|summarize|codeexplain|translate)\b', Keyword.Type),
            # Control Commands
            (r'\b(history|clear|help|exit)\b', Keyword.Builtin),
            # Options
            (r'--?\w+', Name.Attribute),
            # Strings
            (r'"[^"]*"', String.Double),
            (r"'[^']*'", String.Single),
            # Numbers
            (r'\d+', Number.Integer),
            # Paths
            (r'[~/.][\w/.-]*', Name.Variable),
            # Comments
            (r'#.*$', Comment.Single),
            # Everything else
            (r'.', Text),
        ]
    }


class TermIACompleter(Completer):
    """
    Custom completer for TermIA commands with intelligent suggestions.
    """

    def __init__(self):
        """Initialize the completer with command definitions."""
        # Define all commands and their subcommands
        self.commands = {
            # OS Commands
            'ls': {
                'options': ['-a', '-l', '-h', '-la', '-lh', '-lah'],
                'description': 'List files and directories'
            },
            'cd': {
                'options': [],
                'description': 'Change directory'
            },
            'mkdir': {
                'options': ['-p'],
                'description': 'Create directory'
            },
            'pwd': {
                'options': [],
                'description': 'Print working directory'
            },
            'cat': {
                'options': [],
                'description': 'Display file contents'
            },
            # IA Commands
            'ia': {
                'subcommands': ['ask', 'summarize', 'codeexplain', 'translate'],
                'description': 'AI-powered commands'
            },
            # Control Commands
            'history': {
                'options': [],
                'description': 'Show command history'
            },
            'clear': {
                'options': [],
                'description': 'Clear screen'
            },
            'help': {
                'options': [],
                'description': 'Show help'
            },
            'exit': {
                'options': [],
                'description': 'Exit TermIA'
            }
        }

        # IA subcommands with their options
        self.ia_subcommands = {
            'ask': {
                'description': 'Ask a question to AI'
            },
            'summarize': {
                'options': ['--length'],
                'description': 'Summarize text'
            },
            'codeexplain': {
                'description': 'Explain code from file'
            },
            'translate': {
                'options': ['--to'],
                'description': 'Translate text'
            }
        }

        # Language codes for translate
        self.languages = ['pt', 'en', 'es', 'fr', 'de', 'it', 'ja', 'zh', 'ru', 'ar']

        # Summary lengths
        self.summary_lengths = ['short', 'medium', 'long']

    def get_completions(self, document, complete_event):
        """
        Generate completions based on current input.

        Args:
            document: Current document state
            complete_event: Completion event

        Yields:
            Completion objects
        """
        text = document.text_before_cursor
        words = text.split()

        # Empty line - suggest all commands
        if not words or (len(words) == 1 and not text.endswith(' ')):
            word = words[0] if words else ''
            for cmd, info in self.commands.items():
                if cmd.startswith(word):
                    yield Completion(
                        cmd,
                        start_position=-len(word),
                        display=cmd,
                        display_meta=info['description']
                    )

        # Command typed, suggest options or subcommands
        elif len(words) >= 1:
            cmd = words[0]

            # IA command - handle subcommands
            if cmd == 'ia':
                if len(words) == 1 or (len(words) == 2 and not text.endswith(' ')):
                    # Suggest ia subcommands
                    subcmd = words[1] if len(words) > 1 else ''
                    for sub, info in self.ia_subcommands.items():
                        if sub.startswith(subcmd):
                            yield Completion(
                                sub,
                                start_position=-len(subcmd),
                                display=sub,
                                display_meta=info['description']
                            )

                elif len(words) >= 2:
                    # Suggest options for ia subcommands
                    subcmd = words[1]
                    if subcmd in self.ia_subcommands:
                        current = words[-1] if not text.endswith(' ') else ''

                        # For summarize --length
                        if subcmd == 'summarize' and '--length' in words:
                            for length in self.summary_lengths:
                                if length.startswith(current):
                                    yield Completion(
                                        length,
                                        start_position=-len(current),
                                        display=length
                                    )

                        # For translate --to
                        elif subcmd == 'translate' and '--to' in words:
                            for lang in self.languages:
                                if lang.startswith(current):
                                    yield Completion(
                                        lang,
                                        start_position=-len(current),
                                        display=lang
                                    )

                        # Suggest options
                        else:
                            options = self.ia_subcommands[subcmd].get('options', [])
                            for opt in options:
                                if opt.startswith(current):
                                    yield Completion(
                                        opt,
                                        start_position=-len(current),
                                        display=opt
                                    )

            # Regular command - suggest options
            elif cmd in self.commands:
                info = self.commands[cmd]
                current = words[-1] if not text.endswith(' ') else ''

                # Suggest options
                if 'options' in info:
                    for opt in info['options']:
                        if opt.startswith(current):
                            yield Completion(
                                opt,
                                start_position=-len(current),
                                display=opt
                            )

                # For commands that take filenames, suggest files
                if cmd in ['cat', 'cd', 'ia'] and len(words) >= 2:
                    self._suggest_files(current, complete_event, document)

    def _suggest_files(self, prefix, complete_event, document):
        """
        Suggest files and directories based on current prefix.

        Args:
            prefix: Current word being typed
            complete_event: Completion event
            document: Current document
        """
        try:
            # Determine directory to search
            if '/' in prefix or '\\' in prefix:
                directory = os.path.dirname(prefix) or '.'
                file_prefix = os.path.basename(prefix)
            else:
                directory = '.'
                file_prefix = prefix

            # Expand ~ to home
            directory = os.path.expanduser(directory)

            # List files in directory
            if os.path.isdir(directory):
                for item in os.listdir(directory):
                    if item.startswith(file_prefix):
                        full_path = os.path.join(directory, item)
                        is_dir = os.path.isdir(full_path)

                        # Add trailing slash for directories
                        display = item + '/' if is_dir else item

                        yield Completion(
                            item,
                            start_position=-len(file_prefix),
                            display=display,
                            display_meta='directory' if is_dir else 'file'
                        )
        except (OSError, PermissionError):
            # Silently ignore errors
            pass


class EnhancedInputHandler:
    """
    Enhanced input handler with autocomplete, highlighting, and history.
    """

    def __init__(self, history_file: str = '.termia_history'):
        """
        Initialize the enhanced input handler.

        Args:
            history_file: Path to history file
        """
        self.history_file = history_file

        # Create history file if it doesn't exist
        if not os.path.exists(history_file):
            open(history_file, 'a').close()

        # Create prompt session with all features
        self.session = PromptSession(
            history=FileHistory(history_file),
            completer=TermIACompleter(),
            lexer=PygmentsLexer(TermIALexer),
            style=self._create_style(),
            complete_while_typing=True,
            enable_history_search=True,
            mouse_support=False,
        )

    def _create_style(self) -> Style:
        """
        Create custom style for syntax highlighting.

        Returns:
            Style object
        """
        return Style.from_dict({
            # Syntax highlighting colors
            'pygments.keyword.reserved': '#00ff00 bold',      # OS commands (green)
            'pygments.keyword.namespace': '#ffff00 bold',     # ia (yellow)
            'pygments.keyword.type': '#00ffff',               # IA subcommands (cyan)
            'pygments.keyword.builtin': '#ff00ff',            # Control commands (magenta)
            'pygments.name.attribute': '#ffa500',             # Options (orange)
            'pygments.string': '#ff6b6b',                     # Strings (red)
            'pygments.number': '#4ecdc4',                     # Numbers (turquoise)
            'pygments.name.variable': '#95e1d3',              # Paths (light green)
            'pygments.comment': '#888888 italic',             # Comments (gray)

            # Completion menu
            'completion-menu.completion': 'bg:#008888 #ffffff',
            'completion-menu.completion.current': 'bg:#00aaaa #000000 bold',
            'completion-menu.meta.completion': 'bg:#006666 #ffffff',
            'completion-menu.meta.completion.current': 'bg:#008888 #ffffff bold',
        })

    def get_input(self, prompt: str = '> ') -> str:
        """
        Get input from user with all enhanced features.

        Args:
            prompt: Prompt string to display

        Returns:
            User input string
        """
        try:
            return self.session.prompt(prompt)
        except KeyboardInterrupt:
            raise KeyboardInterrupt()
        except EOFError:
            raise EOFError()

    def search_history(self, query: str) -> List[str]:
        """
        Search command history for matching entries.

        Args:
            query: Search query

        Returns:
            List of matching history entries
        """
        try:
            with open(self.history_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            # Filter lines that contain the query
            matches = [line.strip() for line in lines if query.lower() in line.lower()]
            return matches
        except Exception:
            return []


def main():
    """Test function for enhanced input handler."""
    print("=" * 60)
    print("TESTE DO ENHANCED INPUT - TermIA")
    print("=" * 60)
    print("\nFeatures:")
    print("  - Tab: Autocomplete")
    print("  - Up/Down: History navigation")
    print("  - Ctrl+R: History search")
    print("  - Syntax highlighting enabled")
    print("\nType 'exit' to quit\n")

    handler = EnhancedInputHandler('test_history.txt')

    while True:
        try:
            user_input = handler.get_input('TermIA> ')

            if user_input.strip().lower() == 'exit':
                print("Goodbye!")
                break

            if user_input.strip():
                print(f"You typed: {user_input}")

        except KeyboardInterrupt:
            print("\nUse 'exit' to quit")
            continue
        except EOFError:
            print("\nGoodbye!")
            break


if __name__ == '__main__':
    main()
