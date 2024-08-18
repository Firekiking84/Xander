import subprocess

file = open("test/generated_code.py", "w+")
file.write("def test_function():\n\treturn 10\nprint(test_function())")
file.close()

print(subprocess.run(["python", "test/generated_code.py"]).stdout)

file = open("test/generated_code.py", "w+")
file.write("def test_function():\n\treturn 15\nprint(test_function())")
file.close()

print(subprocess.run(["python", "test/generated_code.py"]).stdout)