#!/usr/bin/env python3
"""
Test script for OS commands
"""
import sys
import os

# Add src to path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, 'src')
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

from executor import CommandExecutor

def test_executor():
    """Test all executor commands"""
    print("=" * 60)
    print("TESTE DE COMANDOS DO SO - TermIA")
    print("=" * 60)

    executor = CommandExecutor()

    # Test 1: pwd
    print("\n[TEST 1] pwd")
    try:
        result = executor.execute_pwd()
        print(f"[OK] pwd: {result}")
    except Exception as e:
        print(f"[FAIL] pwd failed: {e}")

    # Test 2: ls
    print("\n[TEST 2] ls")
    try:
        result = executor.execute_ls()
        print(f"[OK] ls:\n{result}")
    except Exception as e:
        print(f"[FAIL] ls failed: {e}")

    # Test 3: ls -la
    print("\n[TEST 3] ls -la")
    try:
        result = executor.execute_ls(options='la')
        lines = result.split('\n')
        print(f"[OK] ls -la (showing first 5 lines):")
        for line in lines[:5]:
            print(f"  {line}")
        if len(lines) > 5:
            print(f"  ... ({len(lines) - 5} more lines)")
    except Exception as e:
        print(f"[FAIL] ls -la failed: {e}")

    # Test 4: mkdir
    print("\n[TEST 4] mkdir test_dir")
    try:
        result = executor.execute_mkdir('test_dir')
        print(f"[OK] mkdir: {result}")
    except FileExistsError:
        print("[OK] mkdir: directory already exists (expected if ran before)")
    except Exception as e:
        print(f"[FAIL] mkdir failed: {e}")

    # Test 5: mkdir -p
    print("\n[TEST 5] mkdir -p test_dir/subdir/deep")
    try:
        result = executor.execute_mkdir('test_dir/subdir/deep', create_parents=True)
        print(f"[OK] mkdir -p: {result}")
    except Exception as e:
        print(f"[FAIL] mkdir -p failed: {e}")

    # Test 6: ls test_dir
    print("\n[TEST 6] ls test_dir")
    try:
        result = executor.execute_ls(path='test_dir')
        print(f"[OK] ls test_dir: {result}")
    except Exception as e:
        print(f"[FAIL] ls test_dir failed: {e}")

    # Test 7: cat README.md
    print("\n[TEST 7] cat README.md")
    try:
        result = executor.execute_cat('README.md')
        print(f"[OK] cat README.md (first 200 chars):")
        print(f"  {result[:200]}...")
    except Exception as e:
        print(f"[FAIL] cat README.md failed: {e}")

    # Test 8: cd test_dir
    print("\n[TEST 8] cd test_dir")
    try:
        result = executor.execute_cd('test_dir')
        print(f"[OK] cd test_dir: {result}")
        # Verify
        print(f"  Current dir: {executor.execute_pwd()}")
    except Exception as e:
        print(f"[FAIL] cd test_dir failed: {e}")

    # Test 9: cd ..
    print("\n[TEST 9] cd ..")
    try:
        result = executor.execute_cd('..')
        print(f"[OK] cd ..: {result}")
        # Verify
        print(f"  Current dir: {executor.execute_pwd()}")
    except Exception as e:
        print(f"[FAIL] cd .. failed: {e}")

    # Test 10: Security test (should block)
    print("\n[TEST 10] Security check (should block)")
    try:
        # This should raise SecurityException
        result = executor.execute_mkdir('rm -rf /')
        print(f"[FAIL] Security FAILED: dangerous command was allowed!")
    except Exception as e:
        print(f"[OK] Security working: {e}")

    print("\n" + "=" * 60)
    print("TESTES CONCLUÍDOS")
    print("=" * 60)

if __name__ == '__main__':
    test_executor()
