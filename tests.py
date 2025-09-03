from functions.run_python_file import run_python_file

# Test Python file execution
print("Testing run_python_file function:\n")

# Test 1: Run main.py without arguments
print('run_python_file("calculator", "main.py"):')
result = run_python_file("calculator", "main.py")
print(result)
print("\n" + "=" * 50 + "\n")

# Test 2: Run main.py with arguments
print('run_python_file("calculator", "main.py", ["3 + 5"]):')
result = run_python_file("calculator", "main.py", ["3 + 5"])
print(result)
print("\n" + "=" * 50 + "\n")

# Test 3: Run tests.py
print('run_python_file("calculator", "tests.py"):')
result = run_python_file("calculator", "tests.py")
print(result)
print("\n" + "=" * 50 + "\n")

# Test 4: Try to run file outside working directory (should error)
print('run_python_file("calculator", "../main.py"):')
result = run_python_file("calculator", "../main.py")
print(result)
print("\n" + "=" * 50 + "\n")

# Test 5: Try to run non-existent file (should error)
print('run_python_file("calculator", "nonexistent.py"):')
result = run_python_file("calculator", "nonexistent.py")
print(result)
print("\n" + "=" * 50 + "\n")
