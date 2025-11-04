import os
from google.genai import types

MAX_CHARS = 10000

def get_file_content(working_directory, file_path):

    # file_path will be relative to working_directory

    file_dir = os.path.join(working_directory, file_path)

    abs_path_working_directory = os.path.abspath(working_directory)

    abs_path_file = os.path.abspath(file_dir)

    if not abs_path_file.startswith(abs_path_working_directory):

        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(abs_path_file):

        return f'Error: File not found or is not a regular file: "{file_path}"'


    try:
        with open(abs_path_file, "r") as f:
            file_content_string = f.read()
            if len(file_content_string) > MAX_CHARS:
                file_content_string = file_content_string[:MAX_CHARS]
                file_content_string += f'[...File "{file_path}" truncated at 10000 characters]'

        return file_content_string

    except FileNotFoundError as e:
        return f"Error: {e}"


schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description=f"Reads and returns the first {MAX_CHARS} characters of the content from a specified file within the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path":types.Schema(
            type=types.Type.STRING,
                description="The path to the file whose content should be read, relative to the working directory.",
            )
        }
    )
)



