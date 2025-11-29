# -*- coding: utf-8 -*-
"""
TermIA - AI Command Executor
This module implements AI-powered commands using external API.
"""

import json
import os
from typing import Dict, Any, Optional
import requests


class AIException(Exception):
    """Exception raised when AI API encounters an error."""
    pass


class AIExecutor:
    """
    AI command executor that integrates with external AI API.
    """

    def __init__(self, api_url: str = None, timeout: int = 30, max_retries: int = 3):
        """
        Initialize the AI executor.

        Args:
            api_url: API endpoint URL (defaults to Ninja Apps API)
            timeout: Request timeout in seconds
            max_retries: Maximum number of retry attempts
        """
        self.api_url = api_url or "https://api.ninja-apps.work/v1/chat/completions"
        self.timeout = timeout
        self.max_retries = max_retries

    def _clean_markdown(self, text: str) -> str:
        """
        Remove common markdown formatting for cleaner terminal display.

        Args:
            text: Text with potential markdown formatting

        Returns:
            Cleaned plain text
        """
        import re

        # Remove bold/italic: **text** or *text* -> text
        text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)
        text = re.sub(r'\*([^*]+)\*', r'\1', text)

        # Remove inline code: `code` -> code
        text = re.sub(r'`([^`]+)`', r'\1', text)

        # Remove headers: ### Header -> Header
        text = re.sub(r'^#{1,6}\s+(.+)$', r'\1', text, flags=re.MULTILINE)

        # Remove horizontal rules: --- or ***
        text = re.sub(r'^[\-*]{3,}$', '', text, flags=re.MULTILINE)

        # Clean up markdown tables (simple approach: keep content, remove formatting)
        # Remove table separators like |---|---|
        text = re.sub(r'^\|[\s\-:|]+\|$', '', text, flags=re.MULTILINE)

        # Convert table rows to simple lines
        text = re.sub(r'^\|\s*(.+?)\s*\|$', r'\1', text, flags=re.MULTILINE)

        # Replace multiple pipes with commas for readability
        text = re.sub(r'\s*\|\s*', ' | ', text)

        # Remove multiple blank lines
        text = re.sub(r'\n\n\n+', '\n\n', text)

        return text.strip()

    def _call_api(self, prompt: str, max_tokens: int = 500, temperature: float = 0.7) -> str:
        """
        Make API call to AI service.

        Args:
            prompt: The prompt/question to send to AI
            max_tokens: Maximum tokens in response
            temperature: Response randomness (0.0-1.0)

        Returns:
            AI response content

        Raises:
            AIException: If API call fails
        """
        # Prepare request data
        data = {
            "messages": json.dumps([{"role": "user", "content": prompt}]),
            "max_tokens": str(max_tokens),
            "temperature": str(temperature)
        }

        # Retry logic
        last_error = None
        for attempt in range(self.max_retries):
            try:
                response = requests.post(
                    self.api_url,
                    data=data,
                    timeout=self.timeout
                )
                response.raise_for_status()

                # Parse response
                result = response.json()

                # Extract content from response
                if "choices" in result and len(result["choices"]) > 0:
                    content = result["choices"][0]["message"]["content"]

                    # Clean up the bot intent/message format if present
                    if "**Bot message:**" in content:
                        # Extract just the message part
                        parts = content.split("**Bot message:**")
                        if len(parts) > 1:
                            return parts[1].strip()

                    return content
                else:
                    raise AIException("Invalid API response format")

            except requests.exceptions.Timeout:
                last_error = f"Request timeout (attempt {attempt + 1}/{self.max_retries})"
                if attempt < self.max_retries - 1:
                    continue
            except requests.exceptions.RequestException as e:
                last_error = f"API request failed: {e}"
                if attempt < self.max_retries - 1:
                    continue
            except json.JSONDecodeError as e:
                last_error = f"Failed to parse API response: {e}"
                break
            except Exception as e:
                last_error = f"Unexpected error: {e}"
                break

        raise AIException(f"AI API call failed after {self.max_retries} attempts: {last_error}")

    # ==================== AI Commands ====================

    def execute_ia_ask(self, question: str) -> str:
        """
        Execute 'ia ask' command - ask a question to AI.

        Args:
            question: Question to ask

        Returns:
            AI response
        """
        if not question or question.strip() == "":
            raise AIException("Question cannot be empty")

        # Detect shell substitution attempts
        if "$(" in question or "${" in question or ("`" in question and question.count("`") >= 2):
            raise AIException(
                "Shell substitution não é suportado no TermIA.\n"
                "  TermIA é um terminal educacional focado em compiladores.\n\n"
                "  Para perguntar sobre arquivos:\n"
                "  • Use: ia codeexplain arquivo.py (para código)\n"
                "  • Ou faça perguntas diretas sobre conceitos"
            )

        # Add instruction for plain text output
        prompt = f"""{question}

IMPORTANTE: Responda em TEXTO PURO para exibicao em terminal.
- NAO use tabelas markdown
- NAO use formatacao markdown (**negrito**, *italico*, etc)
- Use apenas texto simples e listas com "•" ou "-"
- Seja claro e direto"""

        response = self._call_api(prompt, max_tokens=300)
        return self._clean_markdown(response)

    def execute_ia_summarize(self, text: str, length: str = "short") -> str:
        """
        Execute 'ia summarize' command - summarize text.

        Args:
            text: Text to summarize
            length: Summary length (short, medium, long)

        Returns:
            Summary of the text
        """
        if not text or text.strip() == "":
            raise AIException("Text to summarize cannot be empty")

        # Detect shell substitution attempts
        if "$(cat" in text or "${cat" in text or "`cat" in text:
            raise AIException(
                "Shell substitution não é suportado no TermIA.\n"
                "  TermIA é um terminal educacional focado em compiladores.\n\n"
                "  Para resumir conteúdo de arquivo:\n"
                "  1. Use 'cat' para ver o conteúdo\n"
                "  2. Copie o texto\n"
                "  3. Use: ia summarize \"texto copiado\" --length medium\n\n"
                "  Ou considere usar ia ask para perguntas sobre arquivos:\n"
                "  ia ask \"Resuma o conceito principal do README\""
            )

        # Map length to token counts
        length_tokens = {
            "short": 100,
            "medium": 200,
            "long": 400
        }
        max_tokens = length_tokens.get(length.lower(), 150)

        # Build prompt
        if length == "short":
            prompt = f"""Resuma o seguinte texto em no maximo 2-3 frases:

{text}

IMPORTANTE: Responda em TEXTO PURO, sem formatacao markdown."""
        elif length == "medium":
            prompt = f"""Resuma o seguinte texto em um paragrafo:

{text}

IMPORTANTE: Responda em TEXTO PURO, sem formatacao markdown."""
        else:  # long
            prompt = f"""Faca um resumo detalhado do seguinte texto:

{text}

IMPORTANTE: Responda em TEXTO PURO para terminal.
- NAO use formatacao markdown
- Use apenas texto simples e listas com "•" ou "-"
- Organize em paragrafos claros"""

        response = self._call_api(prompt, max_tokens=max_tokens)
        return self._clean_markdown(response)

    def execute_ia_codeexplain(self, filepath: str) -> str:
        """
        Execute 'ia codeexplain' command - explain code from file.

        Args:
            filepath: Path to code file

        Returns:
            Explanation of the code
        """
        # Check for common syntax mistakes
        suspicious_names = ['short', 'medium', 'long', 'pt', 'en', 'es', 'fr', 'de', 'it']
        if filepath.lower() in suspicious_names:
            raise AIException(
                f"'{filepath}' doesn't look like a file path.\n"
                f"  Uso correto: ia codeexplain <arquivo>\n"
                f"  Exemplo: ia codeexplain main.py\n"
                f"  NOTA: Use o caminho do arquivo, não uma string entre aspas!"
            )

        # Read the file
        if not os.path.exists(filepath):
            # Provide helpful error message
            raise AIException(
                f"Arquivo não encontrado: {filepath}\n"
                f"  Certifique-se de que:\n"
                f"  • O arquivo existe no diretório atual\n"
                f"  • O caminho está correto\n"
                f"  • Você não está usando aspas em volta do caminho\n"
                f"  Exemplo correto: ia codeexplain main.py"
            )

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                code = f.read()
        except Exception as e:
            raise AIException(f"Error reading file: {e}")

        if not code.strip():
            raise AIException("File is empty")

        # Limit code size to avoid token limits
        if len(code) > 2000:
            code = code[:2000] + "\n... (truncated)"

        # Build prompt
        file_extension = os.path.splitext(filepath)[1]
        prompt = f"""Explique o seguinte codigo (arquivo {filepath}):

```{file_extension}
{code}
```

IMPORTANTE: Responda em TEXTO PURO para exibicao em terminal.
- NAO use tabelas markdown
- NAO use formatacao markdown (**negrito**, *italico*, etc)
- Use apenas texto simples, paragrafos e listas com "•" ou "-"
- Seja claro e conciso

Forneça uma explicacao do que este codigo faz."""

        response = self._call_api(prompt, max_tokens=500)
        return self._clean_markdown(response)

    def execute_ia_translate(self, text: str, target_language: str) -> str:
        """
        Execute 'ia translate' command - translate text to target language.

        Args:
            text: Text to translate
            target_language: Target language code (pt, en, es, fr, etc.)

        Returns:
            Translated text
        """
        if not text or text.strip() == "":
            raise AIException("Text to translate cannot be empty")

        # Detect shell substitution attempts
        if "$(" in text or "${" in text or ("`" in text and text.count("`") >= 2):
            raise AIException(
                "Shell substitution não é suportado no TermIA.\n"
                "  TermIA é um terminal educacional focado em compiladores.\n\n"
                "  Para traduzir texto:\n"
                "  • Digite o texto diretamente entre aspas\n"
                "  • Exemplo: ia translate \"Hello World\" --to pt"
            )

        # Map language codes to full names
        language_names = {
            "pt": "portugues",
            "en": "ingles",
            "es": "espanhol",
            "fr": "frances",
            "de": "alemao",
            "it": "italiano",
            "ja": "japones",
            "zh": "chines",
            "ru": "russo",
            "ar": "arabe"
        }

        target_lang_name = language_names.get(target_language.lower(), target_language)

        # Build prompt
        prompt = f"Traduza o seguinte texto para {target_lang_name}:\n\n{text}\n\nResponda APENAS com a traducao, sem explicacoes adicionais."

        response = self._call_api(prompt, max_tokens=300)
        return self._clean_markdown(response)


def main():
    """Test function for AI executor."""
    print("=" * 60)
    print("TESTE DO AI EXECUTOR - TermIA")
    print("=" * 60)

    executor = AIExecutor()

    # Test 1: ia ask
    print("\n[TEST 1] ia ask")
    try:
        result = executor.execute_ia_ask("Qual a capital da Franca?")
        print(f"[OK] Response: {result[:100]}...")
    except AIException as e:
        print(f"[FAIL] {e}")

    # Test 2: ia summarize
    print("\n[TEST 2] ia summarize")
    try:
        text = "Python e uma linguagem de programacao de alto nivel, interpretada e de proposito geral. Ela foi criada por Guido van Rossum e lancada em 1991. Python e conhecida por sua sintaxe simples e legivel."
        result = executor.execute_ia_summarize(text, length="short")
        print(f"[OK] Summary: {result}")
    except AIException as e:
        print(f"[FAIL] {e}")

    # Test 3: ia translate
    print("\n[TEST 3] ia translate")
    try:
        result = executor.execute_ia_translate("Hello World", "pt")
        print(f"[OK] Translation: {result}")
    except AIException as e:
        print(f"[FAIL] {e}")

    print("\n" + "=" * 60)
    print("TESTES CONCLUIDOS")
    print("=" * 60)


if __name__ == '__main__':
    main()
