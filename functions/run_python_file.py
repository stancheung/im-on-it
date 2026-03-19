import os
import subprocess

def run_python_file(working_directory, file_path, args=None):
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.normpath(os.path.join(abs_working_dir, file_path))

    if os.path.commonpath([abs_working_dir, abs_file_path]) != abs_working_dir:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not os.path.exists(abs_file_path) or not os.path.isfile(abs_file_path):
        return f'Error: "{file_path}" does not exist or is not a regular file'

    if not file_path.endswith('.py'):
        return f'Error: "{file_path}" is not a Python file'

    command = ["python", abs_file_path]

    if args is not None:
        for arg in args:
            command.extend(arg)

    completed_proc = subprocess.run(command, cwd=abs_working_dir, capture_output=True, text=True, timeout=30)

    rslt = ""
    if completed_proc.returncode != 0:
        rslt += f"Process exited with code {completed_proc.returncode}"
    if completed_proc.stdout == None and completed_proc.stderr == None:
        rslt += f"No output produced"
    elif completed_proc.stdout:
        rslt += f"STDOUT:{completed_proc.stdout}"
    elif completed_proc.stderr:
        rslt += f"STDERR:{completed_proc.stderr}"
    return rslt

run_python_file("calculator", "test.py")
