# TermIA - Enhanced Features Guide

This document describes the advanced features implemented in TermIA.

## Overview

TermIA includes sophisticated features that enhance user experience beyond basic command execution:

- **Intelligent Autocomplete** - Tab-based command and path completion
- **Syntax Highlighting** - Color-coded command syntax as you type
- **Persistent History** - Command history saved between sessions
- **History Search** - Fast search through command history
- **Cross-Platform** - Works on Windows, Linux, and macOS

## Feature Details

### 1. Autocomplete (Tab Completion)

Press `Tab` at any point while typing to get intelligent suggestions.

#### Command Completion
```bash
l<Tab>        # Suggests: ls
h<Tab>        # Suggests: help, history
cd<Tab>       # Suggests options and directories
```

#### Subcommand Completion
```bash
ia <Tab>      # Suggests: ask, summarize, codeexplain, translate
ia s<Tab>     # Suggests: summarize
```

#### Option Completion
```bash
ls -<Tab>         # Suggests: -a, -l, -h, -la, -lh, -lah
ia summarize <Tab> --length
ia translate <Tab> --to
```

#### Path Completion
```bash
cat READ<Tab>     # Suggests: README.md
cd sr<Tab>        # Suggests: src/
```

#### Smart Context-Aware Completion
- After `--length`: suggests `short`, `medium`, `long`
- After `--to`: suggests language codes (`pt`, `en`, `es`, `fr`, etc.)
- Directories shown with trailing `/`
- Files and directories distinguished in completion menu

### 2. Syntax Highlighting

Commands are color-coded as you type for better readability.

#### Color Scheme
- **OS Commands** (ls, cd, mkdir, pwd, cat): Green
- **IA Keyword** (ia): Yellow
- **IA Subcommands** (ask, summarize, etc.): Cyan
- **Control Commands** (history, help, clear, exit): Magenta
- **Options** (--length, --to, -la): Orange
- **Strings** ("text here"): Red
- **Numbers** (10, 20): Turquoise
- **Paths** (./src, ~/docs): Light Green
- **Comments** (# comment): Gray (italic)

#### Example
```bash
ia summarize "This is a text" --length medium
# ↑↑ ↑↑↑↑↑↑↑↑  ↑↑↑↑↑↑↑↑↑↑↑↑↑  ↑↑↑↑↑↑  ↑↑↑↑↑↑
# Yellow Cyan   Red          Orange  text
```

### 3. Command History

TermIA maintains a persistent command history across sessions.

#### Navigating History
- **Up Arrow** (↑): Go to previous command
- **Down Arrow** (↓): Go to next command
- **Home**: Go to beginning of line
- **End**: Go to end of line

#### History Commands
```bash
history          # Show last 10 commands
history 20       # Show last 20 commands
history 100      # Show last 100 commands
```

#### History File
- Location: `.termia_history` (in current directory)
- Format: Plain text, one command per line
- Persistent: History saved between sessions
- Searchable: Use Ctrl+R for incremental search

### 4. History Search (Ctrl+R)

Press `Ctrl+R` to enter reverse history search mode.

```bash
# Press Ctrl+R
(reverse-i-search)`':

# Start typing to search
(reverse-i-search)`ls': ls -la /home/user

# Press Ctrl+R again to cycle through matches
# Press Enter to execute
# Press Ctrl+C to cancel
```

#### Search Tips
- Search is incremental (updates as you type)
- Case-insensitive matching
- Searches through all historical commands
- Highlights matching portion

### 5. Advanced Input Features

#### Keyboard Shortcuts
- **Tab**: Autocomplete
- **Ctrl+A**: Move to beginning of line
- **Ctrl+E**: Move to end of line
- **Ctrl+K**: Delete from cursor to end of line
- **Ctrl+U**: Delete from cursor to beginning of line
- **Ctrl+W**: Delete word before cursor
- **Ctrl+L**: Clear screen
- **Ctrl+C**: Cancel current input
- **Ctrl+D**: Exit (EOF)
- **Ctrl+R**: Reverse history search

#### Multi-line Support
Commands can be edited like in modern IDEs:
- Left/Right arrows: Navigate character by character
- Ctrl+Left/Right: Navigate word by word
- Home/End: Jump to line start/end

### 6. Error Handling

Enhanced input includes robust error handling:

```bash
# Invalid command - clear error message
invalid_cmd
# Erro: tipo de comando desconhecido

# File not found - helpful suggestion
cat nonexistent.txt
# cat: nonexistent.txt: No such file or directory

# Empty AI question - validation
ia ask ""
# Erro de IA: Question cannot be empty
```

## Implementation Details

### Technologies Used
- **prompt_toolkit**: Advanced terminal interface library
- **Pygments**: Syntax highlighting engine
- **PLY**: Lexer/Parser generator

### Architecture

```
EnhancedInputHandler
├── PromptSession (prompt_toolkit)
│   ├── History (FileHistory)
│   ├── Completer (TermIACompleter)
│   ├── Lexer (TermIALexer via Pygments)
│   └── Style (Custom color scheme)
└── Features
    ├── Autocomplete
    ├── Syntax Highlighting
    ├── History Navigation
    └── Search Functionality
```

### Custom Components

#### TermIACompleter
- Implements `Completer` interface
- Context-aware suggestions
- Knows about all commands and their options
- File/directory completion for path arguments

#### TermIALexer
- Extends `RegexLexer` from Pygments
- Custom token definitions for TermIA syntax
- Regex-based pattern matching
- Real-time syntax analysis

#### EnhancedInputHandler
- Wraps prompt_toolkit PromptSession
- Manages history file
- Provides unified interface
- Handles errors gracefully

## Configuration

### Disabling Enhanced Mode
If you encounter compatibility issues:

```python
# In main.py, initialize with enhanced_mode=False
terminal = TermIA(debug_mode=False, enhanced_mode=False)
```

### History File Location
Default: `.termia_history` in current directory

To change:
```python
handler = EnhancedInputHandler('my_custom_history.txt')
```

### Customizing Colors
Edit `enhanced_input.py`, method `_create_style()`:

```python
def _create_style(self) -> Style:
    return Style.from_dict({
        'pygments.keyword.reserved': '#00ff00 bold',  # Change color
        # ... other styles
    })
```

## Troubleshooting

### Issue: Autocomplete not working
**Solution**: Make sure prompt_toolkit is installed:
```bash
pip install prompt_toolkit
```

### Issue: No syntax highlighting
**Solution**: Install Pygments:
```bash
pip install pygments
```

### Issue: History not persisting
**Solution**: Check file permissions for `.termia_history`

### Issue: Terminal compatibility error
**Solution**:
- On Windows: Use cmd.exe or PowerShell instead of Git Bash
- On Linux/Mac: Should work out of the box
- Fallback: Run with `enhanced_mode=False`

## Performance

- **Autocomplete latency**: < 50ms
- **Syntax highlighting**: Real-time (as you type)
- **History search**: O(n) where n = history size
- **Memory usage**: Minimal (history loaded on-demand)

## Future Enhancements

Potential improvements for future versions:
- Fuzzy matching in autocomplete
- Command aliases
- Custom keybindings
- Themes/color schemes
- Command templates
- Smart suggestions based on context
- AI-powered command completion

## References

- [prompt_toolkit Documentation](https://python-prompt-toolkit.readthedocs.io/)
- [Pygments Documentation](https://pygments.org/docs/)
- [PLY Documentation](https://www.dabeaz.com/ply/)
