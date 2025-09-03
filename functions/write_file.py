import os


def write_file(working_directory, file_path, content):
    try:
        # Get absolute paths for proper comparison
        abs_working_dir = os.path.abspath(working_directory)
        full_path = os.path.abspath(os.path.join(working_directory, file_path))

        # Check if the target path is within the working directory
        if not (
            full_path == abs_working_dir
            or full_path.startswith(abs_working_dir + os.sep)
        ):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    except (TypeError, ValueError, OSError) as e:
        return f"Error: Invalid path arguments - {str(e)}"

    try:
        # Create directory if it doesn't exist
        directory = os.path.dirname(full_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)

        # Write the file (creates if doesn't exist, overwrites if it does)
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)

        return (
            f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        )

    except PermissionError:
        return f"Error: Permission denied writing to {file_path}"
    except OSError as e:
        return f"Error: Cannot write to {file_path} - {str(e)}"
