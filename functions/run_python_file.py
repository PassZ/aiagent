import os
import subprocess


def run_python_file(working_directory, file_path, args=[]):
    try:
        # Get absolute paths for proper comparison
        abs_working_dir = os.path.abspath(working_directory)
        full_path = os.path.abspath(os.path.join(working_directory, file_path))

        # Check if the target path is within the working directory
        if not (
            full_path == abs_working_dir
            or full_path.startswith(abs_working_dir + os.sep)
        ):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    except (TypeError, ValueError, OSError) as e:
        return f"Error: Invalid path arguments - {str(e)}"

    # Check if file exists
    if not os.path.exists(full_path):
        return f'Error: File "{file_path}" not found.'

    # Check if file is a Python file
    if not file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'

    try:
        # Run the Python file
        completed_process = subprocess.run(
            ["python3", full_path] + args,
            capture_output=True,
            timeout=30,
            cwd=abs_working_dir,
            text=True,
        )

        # Format output
        stdout_output = completed_process.stdout
        stderr_output = completed_process.stderr

        # Build result string
        result_parts = []

        if stdout_output:
            result_parts.append(f"STDOUT:\n{stdout_output}")

        if stderr_output:
            result_parts.append(f"STDERR:\n{stderr_output}")

        if completed_process.returncode != 0:
            result_parts.append(
                f"Process exited with code {completed_process.returncode}"
            )

        if not stdout_output and not stderr_output:
            return "No output produced."

        return "\n".join(result_parts)

    except subprocess.TimeoutExpired:
        return "Error: executing Python file: Process timed out after 30 seconds"
    except Exception as e:
        return f"Error: executing Python file: {e}"
