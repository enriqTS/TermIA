# -*- coding: utf-8 -*-
"""
TermIA - Command Executor
This module implements safe execution of operating system commands.
"""

import os
import sys
from pathlib import Path
from typing import Optional, Dict, Any
import yaml


class SecurityException(Exception):
    """Exception raised when a command violates security policies."""
    pass


class CommandExecutor:
    """
    Operating system command executor with security checks.
    """

    def __init__(self, config_path: str = "config.yaml"):
        self.current_dir = os.getcwd()
        self.config = self._load_config(config_path)
        self.safe_mode = self.config.get('security', {}).get('safe_mode', True)
        self.restricted_commands = self.config.get('security', {}).get('restricted_commands', [])

    def _load_config(self, config_path: str) -> Dict[str, Any]:
        try:
            if os.path.exists(config_path):
                with open(config_path, 'r', encoding='utf-8') as f:
                    return yaml.safe_load(f) or {}
        except Exception as e:
            print(f"Warning: Could not load config.yaml: {e}")
        return {
            'security': {
                'safe_mode': True,
                'restricted_commands': ['rm -rf /', 'format', 'mkfs']
            }
        }

    def _check_security(self, command: str, path: Optional[str] = None):
        if not self.safe_mode:
            return
        for restricted in self.restricted_commands:
            if restricted.lower() in f"{command} {path or ''}".lower():
                raise SecurityException(f"Command blocked by security: '{restricted}'")

    def _resolve_path(self, path: str) -> str:
        path = os.path.expanduser(path)
        if os.path.isabs(path):
            return path
        return os.path.join(self.current_dir, path)

    def execute_pwd(self) -> str:
        return self.current_dir

    def execute_ls(self, options: Optional[str] = None, path: str = '.') -> str:
        self._check_security('ls', path)
        target_path = self._resolve_path(path)
        if not os.path.exists(target_path):
            raise FileNotFoundError(f"ls: cannot access '{path}': No such file or directory")
        if not os.path.isdir(target_path):
            return os.path.basename(target_path)
        show_hidden = options and 'a' in options
        long_format = options and 'l' in options
        human_readable = options and 'h' in options
        try:
            entries = os.listdir(target_path)
        except PermissionError:
            raise PermissionError(f"ls: cannot open directory '{path}': Permission denied")
        if not show_hidden:
            entries = [e for e in entries if not e.startswith('.')]
        entries.sort()
        if long_format:
            output = []
            for entry in entries:
                entry_path = os.path.join(target_path, entry)
                try:
                    stat = os.stat(entry_path)
                    file_type = 'd' if os.path.isdir(entry_path) else '-'
                    mode = stat.st_mode
                    perms = [
                        'r' if mode & 0o400 else '-', 'w' if mode & 0o200 else '-', 'x' if mode & 0o100 else '-',
                        'r' if mode & 0o040 else '-', 'w' if mode & 0o020 else '-', 'x' if mode & 0o010 else '-',
                        'r' if mode & 0o004 else '-', 'w' if mode & 0o002 else '-', 'x' if mode & 0o001 else '-',
                    ]
                    perms_str = ''.join(perms)
                    size = stat.st_size
                    if human_readable:
                        for unit in ['B', 'KB', 'MB', 'GB']:
                            if size < 1024.0:
                                size_str = f"{size:3.1f}{unit}"
                                break
                            size = size / 1024.0
                    else:
                        size_str = str(stat.st_size)
                    line = f"{file_type}{perms_str} {size_str:>8} {entry}"
                    output.append(line)
                except (OSError, PermissionError):
                    output.append(f"?????????? ? {entry}")
            return '\n'.join(output)
        else:
            return '  '.join(entries)

    def execute_cd(self, path: str = '~') -> str:
        self._check_security('cd', path)
        target_path = self._resolve_path(path)
        if not os.path.exists(target_path):
            raise FileNotFoundError(f"cd: {path}: No such file or directory")
        if not os.path.isdir(target_path):
            raise NotADirectoryError(f"cd: {path}: Not a directory")
        try:
            os.chdir(target_path)
            self.current_dir = os.getcwd()
            return f"Changed directory to: {self.current_dir}"
        except PermissionError:
            raise PermissionError(f"cd: {path}: Permission denied")

    def execute_mkdir(self, path: str, create_parents: bool = False) -> str:
        self._check_security('mkdir', path)
        target_path = self._resolve_path(path)
        if os.path.exists(target_path):
            if create_parents:
                return f"mkdir: directory '{path}' already exists"
            else:
                raise FileExistsError(f"mkdir: cannot create directory '{path}': File exists")
        try:
            if create_parents:
                os.makedirs(target_path, exist_ok=True)
            else:
                os.mkdir(target_path)
            return f"Directory '{path}' created successfully"
        except PermissionError:
            raise PermissionError(f"mkdir: cannot create directory '{path}': Permission denied")
        except OSError as e:
            raise OSError(f"mkdir: cannot create directory '{path}': {e}")

    def execute_cat(self, filepath: str) -> str:
        self._check_security('cat', filepath)
        target_path = self._resolve_path(filepath)
        if not os.path.exists(target_path):
            raise FileNotFoundError(f"cat: {filepath}: No such file or directory")
        if os.path.isdir(target_path):
            raise IsADirectoryError(f"cat: {filepath}: Is a directory")
        try:
            with open(target_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return content
        except PermissionError:
            raise PermissionError(f"cat: {filepath}: Permission denied")
        except UnicodeDecodeError:
            try:
                with open(target_path, 'rb') as f:
                    content = f.read()
                return f"<binary file, {len(content)} bytes>"
            except Exception as e:
                raise Exception(f"cat: error reading file: {e}")
        except Exception as e:
            raise Exception(f"cat: error reading file: {e}")
