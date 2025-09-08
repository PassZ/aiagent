# AI Agent - Intelligent Coding Assistant

An advanced AI-powered coding assistant that can interact with your codebase through function calling. Built with Google's Gemini AI model, this agent can read files, execute Python scripts, write new files, and analyze directory structures to help with coding tasks.

## 🚀 Features

- **File System Operations**: List directories, read file contents, and write new files
- **Code Execution**: Run Python scripts with optional arguments in a sandboxed environment
- **AI-Powered Analysis**: Uses Google Gemini 2.0 Flash for intelligent code understanding and task planning
- **Function Calling**: Implements structured function calling for reliable AI interactions
- **Security**: All operations are constrained to a designated working directory for safety
- **Verbose Mode**: Optional detailed logging for debugging and transparency

## 🛠️ Technology Stack

- **Python 3.12+**
- **Google Gemini AI** (gemini-2.0-flash-001)
- **Function Calling** with structured schemas
- **Environment-based configuration** with python-dotenv

## 📋 Prerequisites

1. **Python 3.12 or higher**
2. **Google Gemini API Key** - Get one from [Google AI Studio](https://makersuite.google.com/app/apikey)
3. **UV package manager** (recommended) or pip

## 🔧 Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd aiagent
```

2. Install dependencies:
```bash
# Using UV (recommended)
uv sync

# Or using pip
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
# Create a .env file in the project root
echo "GEMINI_API_KEY=your_api_key_here" > .env
```

## 🎯 Usage

### Basic Usage
```bash
python main.py "your coding task or question"
```

### Examples

**Analyze a Python file:**
```bash
python main.py "Analyze the calculator.py file and explain what it does"
```

**Create a new script:**
```bash
python main.py "Create a simple hello world script called greet.py"
```

**Run and test code:**
```bash
python main.py "Run the calculator with the expression '2 + 3 * 4' and show me the result"
```

**Explore project structure:**
```bash
python main.py "List all files in the project and tell me about the structure"
```

### Verbose Mode
Add `--verbose` flag for detailed function call information:
```bash
python main.py "Create a fibonacci function" --verbose
```

## 🏗️ Architecture

### Core Components

1. **Main Agent (`main.py`)**
   - Orchestrates AI conversations
   - Manages function calling loop
   - Handles user input and output

2. **Function Modules (`functions/`)**
   - `get_files_info.py` - Directory listing with file metadata
   - `get_file_content.py` - Secure file reading with path validation
   - `run_python_file.py` - Python script execution with timeout protection
   - `write_file.py` - File creation and writing with directory auto-creation

3. **Calculator Example (`calculator/`)**
   - Demonstrates the agent's capabilities
   - Simple calculator with expression evaluation
   - Includes tests and package structure

### Function Calling System

The agent uses Google Gemini's function calling feature with four core capabilities:

- **File Discovery**: List files and directories with metadata
- **Content Reading**: Read file contents with security constraints
- **Code Execution**: Run Python scripts in isolated environment
- **File Writing**: Create and modify files safely

### Security Features

- **Path Validation**: All file operations are constrained to the working directory
- **Timeout Protection**: Script execution limited to 30 seconds
- **Content Limits**: File reading truncated at 10,000 characters
- **Error Handling**: Comprehensive error catching and reporting

## 🧪 Testing

Run the included tests:
```bash
python tests.py
```

Test the calculator example:
```bash
cd calculator
python main.py "2 + 3 * 4"
```

## 📁 Project Structure

```
aiagent/
├── main.py                 # Main agent application
├── functions/              # Function calling modules
│   ├── get_files_info.py
│   ├── get_file_content.py
│   ├── run_python_file.py
│   └── write_file.py
├── calculator/             # Example project for testing
│   ├── main.py
│   ├── pkg/
│   │   ├── calculator.py
│   │   └── render.py
│   └── tests.py
├── pyproject.toml          # Project configuration
├── uv.lock                 # Dependency lock file
└── README.md               # This file
```

## 🔒 Security Considerations

- All file operations are sandboxed to the working directory
- No network access or system-level operations
- Input validation and sanitization
- Timeout protection for script execution
- Path traversal protection

## 🚀 Future Enhancements

- Support for additional programming languages
- Integration with version control systems
- Enhanced code analysis and suggestions
- Multi-file project management
- Custom function definitions

## 📄 License

This project is part of the Boot.dev curriculum and is intended for educational purposes.

## 🤝 Contributing

This is a completed Boot.dev project. For learning purposes, feel free to fork and experiment with the code!

---

**Note**: This AI agent demonstrates advanced function calling capabilities and can serve as a foundation for building more sophisticated coding assistants or automation tools.