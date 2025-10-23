import os

from google.genai import types

def get_files_info(working_directory, directory="."):


    file_dir = os.path.join(working_directory, directory)

    abs_path_working_directory = os.path.abspath(working_directory)

    abs_path_file = os.path.abspath(file_dir)

    if not abs_path_file.startswith(abs_path_working_directory):

        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    if not os.path.isdir(abs_path_file):

        return f'Error: "{directory}" is not a directory'

                
    try:
        list_dir = os.listdir(abs_path_file)


    except OSError as e:

        return f"Error: {e}"
    lines = []

    for dir in list_dir:
        child_path = os.path.join(abs_path_file, dir)

        try:
            lines.append(f"- {dir}: file_size={os.path.getsize(child_path)} bytes, is_dir={os.path.isdir(child_path)}")

        except OSError as e:

            return f"Error: {e}"

    return "\n".join(lines)

schema_get_file_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            )
        }

    )

)



