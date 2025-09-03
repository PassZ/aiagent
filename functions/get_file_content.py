import os


def get_file_content(working_directory, file_path):
    if not os.path.isabs(file_path):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory.'

    if not os.path.isfile(file_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    if os.path.getsize(file_path) > 10000:
        file_content = f'File "{file_path}" truncated at 10000 characters'
    else:
        file_content = open(file_path, "r").read()
    return file_content
