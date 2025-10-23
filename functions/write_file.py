import os
from google.genai import types


def write_file(working_directory, file_path, content):

    file_dir = os.path.join(working_directory, file_path)

    abs_path_working_directory = os.path.abspath(working_directory)

    abs_path_file = os.path.abspath(file_dir)

    print(abs_path_file)

    if not abs_path_file.startswith(abs_path_working_directory):

        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    try:
        with open(abs_path_file, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except FileNotFoundError as e:
        return f"Error: {e}"

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writing the content to the file in the file path directory which is relative to the working directory. If the file doesn't exist it will create the file on the declared file path",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path" : types.Schema(
                type=types.Type.STRING,
                description="The directory of the file relative to the working directory."
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write in the dedicated file in the file path"
            )
        }
    )

)

