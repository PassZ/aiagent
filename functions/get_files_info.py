import os
from google.genai import types


def get_files_info(working_directory, directory="."):
    print(f"Result for '{directory}' directory:")

    try:
        abs_working_dir = os.path.abspath(working_directory)
        full_path = os.path.abspath(os.path.join(working_directory, directory))

        if not (
            full_path == abs_working_dir
            or full_path.startswith(abs_working_dir + os.sep)
        ):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    except (TypeError, ValueError, OSError) as e:
        return f"Error: Invalid path arguments - {str(e)}"

    try:
        if not os.path.isdir(full_path):
            return f"Error: {directory} is not a directory"
    except (PermissionError, OSError) as e:
        return f"Error: Cannot access {directory} - {str(e)}"

    file_info = ""
    try:
        files = os.listdir(full_path)
    except PermissionError:
        return f"Error: Permission denied accessing {directory}"
    except FileNotFoundError:
        return f"Error: Directory {directory} not found"
    except OSError as e:
        return f"Error: Cannot list directory {directory} contents - {str(e)}"

    for file in files:
        if file.startswith(".") or file == "__pycache__":
            continue

        try:
            file_path = os.path.join(full_path, file)
            if os.path.isfile(file_path):
                file_info += f"- {file}: file_size={os.path.getsize(file_path)} bytes, is_dir=False\n"
            elif os.path.isdir(file_path):
                file_info += f"- {file}: file_size=N/A bytes, is_dir=True\n"

        except PermissionError:
            file_info += f"- {file}: Error - Permission denied\n"
        except OSError as e:
            file_info += f"- {file}: Error - {str(e)}\n"

    return file_info


# Function declaration (schema) for "get_files_info"
schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description=(
        "Lists files in the specified directory along with their sizes, "
        "constrained to the working directory."
    ),
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description=(
                    "The directory to list files from, relative to the working directory. "
                    "If not provided, lists files in the working directory itself."
                ),
            ),
        },
    ),
)
