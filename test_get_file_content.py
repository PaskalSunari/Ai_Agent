from functions.get_file_content import get_file_content


# Modification: test reading main.py.
print("Result for 'main.py':")
print(get_file_content("calculator", "main.py"))


# Modification: test reading a file inside the pkg directory.
print("Result for 'pkg/calculator.py':")
print(get_file_content("calculator", "pkg/calculator.py"))


# Modification: test a file outside the permitted working directory.
print("Result for '/bin/cat':")
print(get_file_content("calculator", "/bin/cat"))


# Modification: test a file that does not exist.
print("Result for 'pkg/does_not_exist.py':")
print(get_file_content("calculator", "pkg/does_not_exist.py"))


result = get_file_content("calculator", "lorem.txt")

print(f"lorem.txt length: {len(result)}")
print(f"lorem.txt truncated: {'truncated' in result}")