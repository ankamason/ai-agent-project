#!/usr/bin/env python3
"""
Test script for get_files_info function.
This tests the AI agent's file system capabilities.
"""

from functions.get_files_info import get_files_info


def main():
    print("🧪 Testing AI Agent File System Capabilities")
    print("=" * 50)
    print()
    
    # Test 1: List current directory contents relative to calculator
    print("Test 1: List calculator directory contents")
    print("Command: get_files_info('calculator', '.')")
    result1 = get_files_info("calculator", ".")
    print("Result:")
    print(result1)
    print()
    print("-" * 40)
    print()
    
    # Test 2: List pkg subdirectory
    print("Test 2: List calculator/pkg directory contents")
    print("Command: get_files_info('calculator', 'pkg')")
    result2 = get_files_info("calculator", "pkg")
    print("Result:")
    print(result2)
    print()
    print("-" * 40)
    print()
    
    # Test 3: Try to access /bin (should fail - security test)
    print("Test 3: Try to access /bin (security test - should fail)")
    print("Command: get_files_info('calculator', '/bin')")
    result3 = get_files_info("calculator", "/bin")
    print("Result:")
    print(result3)
    print()
    print("-" * 40)
    print()
    
    # Test 4: Try to access parent directory (should fail - security test)
    print("Test 4: Try to access parent directory (security test - should fail)")
    print("Command: get_files_info('calculator', '../')")
    result4 = get_files_info("calculator", "../")
    print("Result:")
    print(result4)
    print()
    print("-" * 40)
    print()
    
    # Bonus Test 5: Test main project directory
    print("Bonus Test 5: List main project directory")
    print("Command: get_files_info('.', '.')")
    result5 = get_files_info(".", ".")
    print("Result:")
    print(result5)
    print()
    print("=" * 50)
    print("🎉 All tests completed!")


if __name__ == "__main__":
    main()
