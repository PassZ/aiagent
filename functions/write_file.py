import os
from google.genai import types


def write_file(working_directory, file_path, content):
    """
    Writes content to a file, creating it if it doesn't exist or overwriting if it does.
    Constrained to the working directory.
    """
    try:
        abs_working_dir = os.path.abspath(working_directory)
        full_path = os.path.abspath(os.path.join(working_directory, file_path))

        if not (
            full_path == abs_working_dir
            or full_path.startswith(abs_working_dir + os.sep)
        ):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    except (TypeError, ValueError, OSError) as e:
        return f"Error: Invalid path arguments - {str(e)}"

    try:
        # Create directory if it doesn't exist
        dir_path = os.path.dirname(full_path)
        if dir_path and not os.path.exists(dir_path):
            os.makedirs(dir_path, exist_ok=True)

        # Write the file
        with open(full_path, 'w', encoding='utf-8') as file:
            file.write(content)
        
        return f"Successfully wrote {len(content)} characters to {file_path}"

    except PermissionError:
        return f"Error: Permission denied writing to {file_path}"
    except OSError as e:
        return f"Error: Cannot write to file {file_path} - {str(e)}"


# Function declaration (schema) for "write_file"
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description=(
        "Writes content to a file, creating it if it doesn't exist or overwriting if it does. "
        "Constrained to the working directory."
    ),
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description=(
                    "The path to the file to write to, relative to the working directory."
                ),
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description=(
                    "The content to write to the file."
                ),
            ),
        },
        required=["file_path", "content"],
    ),
)