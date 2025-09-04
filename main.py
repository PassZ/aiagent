import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info, get_files_info
from functions.get_file_content import schema_get_file_content, get_file_content
from functions.run_python_file import schema_run_python_file, run_python_file
from functions.write_file import schema_write_file, write_file

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file,
    ]
)

# Dictionary mapping function names to their implementations
function_map = {
    "get_files_info": get_files_info,
    "get_file_content": get_file_content,
    "run_python_file": run_python_file,
    "write_file": write_file,
}


def call_function(function_call_part, verbose=False):
    """
    Handle the abstract task of calling one of our four functions.
    
    Args:
        function_call_part: A types.FunctionCall with .name and .args properties
        verbose: If True, print detailed information about the function call
    
    Returns:
        types.Content with the function result or error
    """
    function_name = function_call_part.name
    function_args = dict(function_call_part.args or {})
    
    # Add working_directory to the arguments
    function_args["working_directory"] = "./calculator"
    
    if verbose:
        print(f"Calling function: {function_name}({function_args})")
    else:
        print(f" - Calling function: {function_name}")
    
    # Check if function exists
    if function_name not in function_map:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )
    
    # Call the function
    try:
        function_result = function_map[function_name](**function_args)
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"result": function_result},
                )
            ],
        )
    except Exception as e:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Function execution failed: {str(e)}"},
                )
            ],
        )


def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <prompt> [--verbose]")
        sys.exit(1)

    # Parse command line arguments
    verbose = "--verbose" in sys.argv
    # Filter out --verbose from arguments to get the prompt
    prompt_args = [arg for arg in sys.argv[1:] if arg != "--verbose"]
    
    if not prompt_args:
        print("Usage: python main.py <prompt> [--verbose]")
        sys.exit(1)
    
    user_prompt = " ".join(prompt_args)

    messages = [
        types.Content(
            role="user",
            parts=[types.Part(text=user_prompt)],
        )
    ]

    # Conversation loop with max 20 iterations
    max_iterations = 20
    for iteration in range(max_iterations):
        try:
            response = client.models.generate_content(
                model="gemini-2.0-flash-001",
                contents=messages,
                config=types.GenerateContentConfig(
                    tools=[available_functions], system_instruction=system_prompt
                ),
            )

            # Add each candidate's content to messages
            if hasattr(response, 'candidates') and response.candidates:
                for candidate in response.candidates:
                    if hasattr(candidate, 'content') and candidate.content:
                        messages.append(candidate.content)

            # Check if we have function calls to execute
            if getattr(response, "function_calls", None):
                function_responses = []
                
                for fc in response.function_calls:
                    # Use call_function to handle the function call
                    function_call_result = call_function(fc, verbose=verbose)
                    
                    # Validate the response structure
                    if not (function_call_result.parts and 
                           len(function_call_result.parts) > 0 and 
                           hasattr(function_call_result.parts[0], 'function_response') and
                           function_call_result.parts[0].function_response and
                           hasattr(function_call_result.parts[0].function_response, 'response')):
                        raise RuntimeError("Invalid function call result structure")
                    
                    # Print result if verbose
                    if verbose:
                        print(f"-> {function_call_result.parts[0].function_response.response}")
                    
                    # Collect function responses
                    function_responses.extend(function_call_result.parts)
                
                # Add function responses as user message
                if function_responses:
                    messages.append(types.Content(
                        role="user",
                        parts=function_responses
                    ))
                
                # Continue the loop to let the LLM process the function results
                continue
            
            # Check if we have a final text response
            if hasattr(response, 'text') and response.text:
                print("Final response:")
                print(response.text.strip())
                break
                
        except Exception as e:
            print(f"Error during conversation: {e}")
            break
    
    else:
        print(f"Reached maximum iterations ({max_iterations}). Stopping.")


if __name__ == "__main__":
    main()
