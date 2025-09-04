import os
import subprocess
import sys
from google.genai import types


def run_python_file(working_directory, file_path, args=None):
    """
    Executes a Python file with optional arguments, constrained to the working directory.
    """
    try:
        abs_working_dir = os.path.abspath(working_directory)
        full_path = os.path.abspath(os.path.join(working_directory, file_path))

        if not (
            full_path == abs_working_dir
            or full_path.startswith(abs_working_dir + os.sep)
        ):
            return f'Error: Cannot run "{file_path}" as it is outside the permitted working directory'

    except (TypeError, ValueError, OSError) as e:
        return f"Error: Invalid path arguments - {str(e)}"

    try:
        if not os.path.isfile(full_path):
            return f"Error: {file_path} is not a file or does not exist"
    except (PermissionError, OSError) as e:
        return f"Error: Cannot access {file_path} - {str(e)}"

    if not file_path.endswith('.py'):
        return f"Error: {file_path} is not a Python file"

    try:
        # Prepare command
        cmd = [sys.executable, full_path]
        if args:
            cmd.extend(args)

        # Run the Python file
        result = subprocess.run(
            cmd,
            cwd=working_directory,
            capture_output=True,
            text=True,
            timeout=30  # 30 second timeout
        )

        output = ""
        if result.stdout:
            output += f"STDOUT:\n{result.stdout}\n"
        if result.stderr:
            output += f"STDERR:\n{result.stderr}\n"
        if result.returncode != 0:
            output += f"Exit code: {result.returncode}\n"

        return output.strip() if output else "Script executed successfully with no output"

    except subprocess.TimeoutExpired:
        return f"Error: Script {file_path} timed out after 30 seconds"
    except PermissionError:
        return f"Error: Permission denied executing {file_path}"
    except OSError as e:
        return f"Error: Cannot execute file {file_path} - {str(e)}"


# Function declaration (schema) for "run_python_file"
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description=(
        "Executes a Python file with optional arguments, "
        "constrained to the working directory."
    ),
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description=(
                    "The path to the Python file to execute, relative to the working directory."
                ),
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description=(
                    "Optional list of command-line arguments to pass to the Python script."
                ),
            ),
        },
        required=["file_path"],
    ),
)