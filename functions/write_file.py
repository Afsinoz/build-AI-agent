import os


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





    
