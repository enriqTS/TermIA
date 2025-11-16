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

        prompt = question
        return self._call_api(prompt, max_tokens=300)

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

        # Map length to token counts
        length_tokens = {
            "short": 100,
            "medium": 200,
            "long": 400
        }
        max_tokens = length_tokens.get(length.lower(), 150)

        # Build prompt
        if length == "short":
            prompt = f"Resuma o seguinte texto em no maximo 2-3 frases:\n\n{text}"
        elif length == "medium":
            prompt = f"Resuma o seguinte texto em um paragrafo:\n\n{text}"
        else:  # long
            prompt = f"Faca um resumo detalhado do seguinte texto:\n\n{text}"

        return self._call_api(prompt, max_tokens=max_tokens)

    def execute_ia_codeexplain(self, filepath: str) -> str:
        """
        Execute 'ia codeexplain' command - explain code from file.

        Args:
            filepath: Path to code file

        Returns:
            Explanation of the code
        """
        # Read the file
        if not os.path.exists(filepath):
            raise AIException(f"File not found: {filepath}")

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
        prompt = f"Explique o seguinte codigo (arquivo {filepath}):\n\n```{file_extension}\n{code}\n```\n\nForneça uma explicacao clara e concisa do que este codigo faz."

        return self._call_api(prompt, max_tokens=500)

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

        return self._call_api(prompt, max_tokens=300)


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
