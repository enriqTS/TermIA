#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for AI commands
"""
import sys
import os

# Add src to path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, 'src')
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

from ai_executor import AIExecutor, AIException

def test_ai_executor():
    """Test all AI executor commands"""
    print("=" * 60)
    print("TESTE DE COMANDOS DE IA - TermIA")
    print("=" * 60)

    executor = AIExecutor()

    # Test 1: ia ask
    print("\n[TEST 1] ia ask - Simple question")
    try:
        result = executor.execute_ia_ask("What is 2+2?")
        print(f"[OK] ia ask")
        print(f"  Question: What is 2+2?")
        print(f"  Answer: {result[:100]}")
    except AIException as e:
        print(f"[FAIL] ia ask failed: {e}")
    except Exception as e:
        print(f"[FAIL] ia ask error: {e}")

    # Test 2: ia summarize - short
    print("\n[TEST 2] ia summarize - Short summary")
    try:
        text = "Python is a high-level programming language. It was created by Guido van Rossum and first released in 1991. Python is known for its simple and readable syntax."
        result = executor.execute_ia_summarize(text, length="short")
        print(f"[OK] ia summarize (short)")
        print(f"  Original length: {len(text)} chars")
        print(f"  Summary length: {len(result)} chars")
    except AIException as e:
        print(f"[FAIL] ia summarize failed: {e}")
    except Exception as e:
        print(f"[FAIL] ia summarize error: {e}")

    # Test 3: ia translate
    print("\n[TEST 3] ia translate - English to Portuguese")
    try:
        result = executor.execute_ia_translate("Hello, how are you?", "pt")
        print(f"[OK] ia translate")
        print(f"  Original: Hello, how are you?")
        print(f"  Translated: {result[:100]}")
    except AIException as e:
        print(f"[FAIL] ia translate failed: {e}")
    except Exception as e:
        print(f"[FAIL] ia translate error: {e}")

    # Test 4: ia codeexplain
    print("\n[TEST 4] ia codeexplain - Analyze test file")
    try:
        # Create a simple test file
        test_file = "test_code_sample.py"
        with open(test_file, 'w') as f:
            f.write('def hello():\n    print("Hello World")\n')

        result = executor.execute_ia_codeexplain(test_file)
        print(f"[OK] ia codeexplain")
        print(f"  File: {test_file}")
        print(f"  Explanation length: {len(result)} chars")

        # Cleanup
        os.remove(test_file)
    except AIException as e:
        print(f"[FAIL] ia codeexplain failed: {e}")
    except Exception as e:
        print(f"[FAIL] ia codeexplain error: {e}")

    # Test 5: Error handling - empty question
    print("\n[TEST 5] Error handling - Empty question")
    try:
        result = executor.execute_ia_ask("")
        print(f"[FAIL] Should have raised AIException for empty question")
    except AIException as e:
        print(f"[OK] Correctly raised AIException: {e}")
    except Exception as e:
        print(f"[FAIL] Unexpected error: {e}")

    print("\n" + "=" * 60)
    print("TESTES CONCLUIDOS")
    print("=" * 60)
    print("\nNote: AI responses may vary. Tests check functionality, not content.")

if __name__ == '__main__':
    test_ai_executor()
