import os 

directory = "./"



abs_path = os.path.abspath(directory)

list_dir = os.listdir(abs_path)

for file_dir in list_dir:
    abs_file_dir = os.path.abspath(file_dir)
    print(f"- {file_dir}: file_size={os.path.getsize(abs_file_dir)} bytes, is_dir={not os.path.isfile(abs_file_dir)} ")




