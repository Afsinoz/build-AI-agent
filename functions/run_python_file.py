import os 
import sys
import subprocess

from google.genai import types


def run_python_file(working_directory, file_path, args=None):
    
    file_dir = os.path.join(working_directory, file_path)

    abs_path_working_dir = os.path.abspath(working_directory)

    abs_path_file = os.path.abspath(file_dir)

    if not abs_path_file.startswith(abs_path_working_dir):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not os.path.exists(abs_path_file):
        return f'Error: File "{file_path}" not found.'
    
    if not abs_path_file.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'

    try:
        commands = [sys.executable, abs_path_file]
        if args:
            commands.extend(args)
        
        results = subprocess.run(commands,
                                 timeout=30, 
                                 capture_output=True, 
                                 text=True,
                                 cwd=abs_path_working_dir)

        output = []

        if results.stdout:
            output.append(f"STDOUT:\n{results.stdout}")
        if results.stderr:
            output.append(f"STDERR:\n{results.stderr}")


        if results.returncode != 0:
            output.append(f"""
            Process exited with code {results.returncode}
            """)

        return "\n".join(output) if output else "No output produced."

    except Exception as e:
        return f"Error: executing Python file: {e}"


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Run the python files in the file path directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
            type=types.Type.STRING,
            description="The file path of the python file, relative to the working directory. If not provided, it won't work."
            ),
            "args": types.Schema(
            type=types.Type.ARRAY,
            description="Optional list of arguments that will be run with the dedicated python script. If not provided, args will be none.",
            items=types.Schema(type=types.Type.STRING)
            )
        },
        required=["file_path"]
    )


)

