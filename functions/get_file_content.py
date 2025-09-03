import os
from .config import MAX_FILE_SIZE_CHARS


def get_file_content(working_directory, file_path):
    try:
        # Get absolute paths for proper comparison
        abs_working_dir = os.path.abspath(working_directory)
        full_path = os.path.abspath(os.path.join(working_directory, file_path))

        # Check if the target path is within the working directory
        if not (
            full_path == abs_working_dir
            or full_path.startswith(abs_working_dir + os.sep)
        ):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    except (TypeError, ValueError, OSError) as e:
        return f"Error: Invalid path arguments - {str(e)}"

    try:
        if not os.path.isfile(full_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
    except (PermissionError, OSError) as e:
        return f"Error: Cannot access file {file_path} - {str(e)}"

    try:
        with open(full_path, "r", encoding="utf-8") as file:
            content = file.read()

        if len(content) > MAX_FILE_SIZE_CHARS:
            content = content[:MAX_FILE_SIZE_CHARS]
            content += (
                f'[...File "{file_path}" truncated at {MAX_FILE_SIZE_CHARS} characters]'
            )

        return content

    except PermissionError:
        return f"Error: Permission denied reading file {file_path}"
    except UnicodeDecodeError:
        return f"Error: Cannot decode file {file_path} - file may be binary"
    except OSError as e:
        return f"Error: Cannot read file {file_path} - {str(e)}"
