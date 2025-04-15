# tOAI

A lightweight Python CLI and library for interacting with custom OpenAI API endpoints.

## Features

- Dual mode: Use as a CLI tool or import as a library
- Minimal dependencies
- Customizable API endpoints and providers
- Streaming responses
- Web search capability (supported by compatible API endpoints)
- Cross-platform configuration system
- Experimental features:
  - Shell command generation and execution (OS-aware)
  - Code generation with clean output

## Installation

```bash
pip install tOAI
```

## Usage

### As a CLI Tool

```bash
# Basic chat (default mode)
tOAI "Hello, how are you?"

# Show version information
tOAI -v

# With custom options
tOAI --api-key your-key --base-url http://your-endpoint "Hello"

# Enable web search (if your API endpoint supports it)
tOAI --web-search "What's the latest news about AI?"

# Generate and execute shell commands (using -s or --shell flag)
tOAI -s "list all files in current directory"

# Generate code (using -c or --code flag)
tOAI -c "create a python function that calculates fibonacci numbers"
```

### As a Library

```python
from tOAI import TOAIClient, load_config

# Load from config file
config = load_config()

# Initialize the client with config
client = TOAIClient(**config)

# Or initialize with custom parameters
client = TOAIClient(
    api_key="your-key",
    base_url="http://your-endpoint",
    provider="openai",
    model="o3-mini"
)

# Chat
response = client.chat("Hello, how are you?")

# Chat with web search (if your API endpoint supports it)
response = client.chat("What's the latest news about AI?", web_search=True)

# Generate shell command
command = client.generate_shell_command("list all files")

# Generate code
code = client.generate_code("create a python function that calculates fibonacci numbers")
```

## Configuration

### Command Line Options

You can configure the client using the following options:

- `--api-key`: API key for the service
- `--base-url`: Base URL for the API
- `--provider`: Provider name
- `--model`: Model to use
- `--web-search`: Enable web search capability (Note: Your API endpoint must support this feature)
- `--config`: Path to a custom configuration file

### Configuration File

tOAI uses a configuration file stored in the standard user config directory for your operating system:

- **Linux**: `~/.config/tOAI/tOAI.conf` or `$XDG_CONFIG_HOME/tOAI/tOAI.conf`
- **macOS**: `~/Library/Application Support/tOAI/tOAI.conf`
- **Windows**: `%APPDATA%\tOAI\tOAI.conf`

The configuration file uses JSON format:

#### OpenAI API Example
```json
{
  "api_key": "your_openai_api_key_here",
  "base_url": "https://api.openai.com/v1/",
  "provider": "OpenAI",
  "model": "gpt-3.5-turbo"
}
```

#### Custom Endpoint Example
```json
{
  "api_key": "your_api_key_here",
  "base_url": "http://127.0.0.1:1337/v1/",
  "provider": "Blackbox",
  "model": "DeepSeek-V3"
}
```

### Configuration Priority

tOAI determines configuration values in the following order (highest priority first):

1. Command line arguments
2. Environment variables (`OPENAI_API_KEY`, `OPENAI_BASE_URL`, `OPENAI_PROVIDER`, `OPENAI_MODEL`)
3. Configuration file
4. Default values

## Special Features

### OS-Aware Shell Commands

Shell command generation is OS-aware, providing appropriate commands for your operating system (Windows, macOS, or Linux) and shell type (bash, powershell, etc.).

### Clean Code Generation

Code generation uses an improved prompt that ensures only clean code is returned, without markdown formatting or unnecessary explanations.

## Implementation Notes

This library uses direct HTTP requests instead of the OpenAI client library, allowing it to work with custom API endpoints that support additional parameters like `provider` and `web_search`. All parameters are sent directly in the request body, similar to the format shown in the curl example.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.