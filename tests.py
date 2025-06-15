from functions.get_file_content import get_file_content

def test_get_file_content():
    """Test the get_file_content function with various scenarios"""
    
    print("Testing get_file_content function...\n")
    
    # Test 1: Read main.py from calculator directory
    print("Test 1: Reading calculator/main.py")
    content = get_file_content("calculator", "main.py")
    if content.startswith("Error:"):
        print(f"  ❌ {content}")
    else:
        print(f"  ✅ Successfully read main.py ({len(content)} characters)")
        print("  File contents:")
        print(content)
    print()
    
    # Test 2: Read calculator.py from pkg subdirectory
    print("Test 2: Reading calculator/pkg/calculator.py")
    content = get_file_content("calculator", "pkg/calculator.py")
    if content.startswith("Error:"):
        print(f"  ❌ {content}")
    else:
        print(f"  ✅ Successfully read pkg/calculator.py ({len(content)} characters)")
        # Show the full content since it contains the apply_operator method
        print("  File contents:")
        print(content)
    print()
    
    # Test 3: Try to read file outside working directory (should fail)
    print("Test 3: Attempting to read /bin/cat (outside working directory)")
    content = get_file_content("calculator", "/bin/cat")
    if content.startswith("Error:"):
        print(f"  ✅ Correctly blocked: {content}")
    else:
        print(f"  ❌ Security issue: Should not be able to read files outside working directory!")
    print()
    
    # Test 4: Try to read non-existent file
    print("Test 4: Attempting to read non-existent file")
    content = get_file_content("calculator", "this_file_does_not_exist.txt")
    if content.startswith("Error:"):
        print(f"  ✅ Correctly reported error: {content}")
    else:
        print(f"  ❌ Should have reported file not found!")
    print()
    
    # Test 5: Try to read a directory instead of a file
    print("Test 5: Attempting to read a directory")
    content = get_file_content("calculator", "pkg")
    if content.startswith("Error:"):
        print(f"  ✅ Correctly reported error: {content}")
    else:
        print(f"  ❌ Should have reported that pkg is not a regular file!")
    print()
    
    # Test 6: Test file truncation with lorem.txt
    print("Test 6: Testing truncation with lorem.txt")
    content = get_file_content("calculator", "lorem.txt")
    if content.startswith("Error:"):
        print(f"  ❌ {content}")
    else:
        if "[...File" in content and "truncated at 10000 characters]" in content:
            print(f"  ✅ Successfully truncated large file")
            print(f"  Total length (including truncation message): {len(content)} characters")
        else:
            print(f"  ❌ File should have been truncated but wasn't")
    print()

if __name__ == "__main__":
    test_get_file_content()
