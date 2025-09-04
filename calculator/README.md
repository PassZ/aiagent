# AI Assistant - Code Documentation and Execution

## Description

This project implements an AI assistant capable of documenting and executing code. It provides functionalities for listing files, reading file contents, running Python files, and writing to files. This assistant is designed to help users understand and interact with code repositories. This particular instance is designed to function as an agent capable of exploring its environment and modifying files.

## Usage

The AI assistant is controlled through a set of API calls. There is no direct user interface. The core functionalities are:

*   **Listing Files:** You can explore the file structure of the repository using the `get_files_info` API call.
*   **Reading Files:** You can read the content of any file within the repository using the `get_file_content` API call.
*   **Executing Python Files:** You can execute Python scripts with optional arguments using the `run_python_file` API call.
*   **Writing Files:** You can create new files or modify existing ones using the `write_file` API call.

## Directory Structure

*   `README.md`: The current documentation file.
*   `main.py`: The main entry point of the AI assistant. It handles the execution of Python files and interacts with the core functionalities. In essence, it's a simple calculator application.
*   `pkg/`: This directory contains modules used by `main.py`:
    *   `calculator.py`: Contains the `Calculator` class, responsible for evaluating mathematical expressions.
    *   `render.py`: Contains the `render` function, responsible for formatting the output.
*   `tests.py`: Contains unit tests for the project.

## Files

*   `calculator.py`: A simple calculator program which can be called by main.py.
*   `lorem.txt`: A simple text file.

## Example

To run the `main.py` calculator:

```bash
python main.py "<expression>"
```

For example:

```bash
python main.py "1 + 1"
```

This command will execute the `main.py` file with the expression "1 + 1" and print the result. The `main.py` script uses the `Calculator` class from `pkg/calculator.py` to evaluate the expression and the `render` function from `pkg/render.py` to format the output.

## Notes

*   All file paths are relative to the root directory of the project.
*   The AI assistant has limited capabilities and is still under development.
*   The `main.py` script takes a mathematical expression as a command-line argument, evaluates it using the `Calculator` class, and prints the result.
