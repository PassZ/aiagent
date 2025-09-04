import os
from google.genai import types


def get_file_content(working_directory, file_path):
    """
    Reads and returns the contents of a file, constrained to the working directory.
    """
    try:
        abs_working_dir = os.path.abspath(working_directory)
        full_path = os.path.abspath(os.path.join(working_directory, file_path))

        if not (
            full_path == abs_working_dir
            or full_path.startswith(abs_working_dir + os.sep)
        ):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    except (TypeError, ValueError, OSError) as e:
        return f"Error: Invalid path arguments - {str(e)}"

    try:
        if not os.path.isfile(full_path):
            return f"Error: {file_path} is not a file or does not exist"
    except (PermissionError, OSError) as e:
        return f"Error: Cannot access {file_path} - {str(e)}"

    try:
        with open(full_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Truncate content if it exceeds 10,000 characters
        if len(content) > 10000:
            content = content[:10000] + "\n... (truncated)"
        
        return content
    except PermissionError:
        return f"Error: Permission denied reading {file_path}"
    except UnicodeDecodeError:
        return f"Error: Cannot decode {file_path} as UTF-8 text"
    except OSError as e:
        return f"Error: Cannot read file {file_path} - {str(e)}"


# Function declaration (schema) for "get_file_content"
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description=(
        "Reads and returns the contents of a file, "
        "constrained to the working directory."
    ),
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description=(
                    "The path to the file to read, relative to the working directory."
                ),
            ),
        },
        required=["file_path"],
    ),
)