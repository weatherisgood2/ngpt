# nGPT

A lightweight Python CLI and library for interacting with OpenAI-compatible APIs, supporting both official and self-hosted LLM endpoints.

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
pip install ngpt
```

## Usage

### As a CLI Tool

```bash
# Basic chat (default mode)
ngpt "Hello, how are you?"

# Show version information
ngpt -v

# Show active configuration
ngpt --show-config

# Show all configurations
ngpt --show-config --all

# With custom options
ngpt --api-key your-key --base-url http://your-endpoint "Hello"

# Enable web search (if your API endpoint supports it)
ngpt --web-search "What's the latest news about AI?"

# Generate and execute shell commands (using -s or --shell flag)
ngpt -s "list all files in current directory"

# Generate code (using -c or --code flag)
ngpt -c "create a python function that calculates fibonacci numbers"
```

### As a Library

```python
from ngpt import NGPTClient, load_config

# Load the first configuration (index 0) from config file
config = load_config(config_index=0)

# Initialize the client with config
client = NGPTClient(**config)

# Or initialize with custom parameters
client = NGPTClient(
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
- `--model`: Model to use
- `--web-search`: Enable web search capability (Note: Your API endpoint must support this feature)
- `--config`: Path to a custom configuration file
- `--config-index`: Index of the configuration to use from the config file (default: 0)
- `--show-config`: Show configuration details and exit.
- `--all`: Used with `--show-config` to display details for all configurations.

### Configuration File

nGPT uses a configuration file stored in the standard user config directory for your operating system:

- **Linux**: `~/.config/ngpt/ngpt.conf` or `$XDG_CONFIG_HOME/ngpt/ngpt.conf`
- **macOS**: `~/Library/Application Support/ngpt/ngpt.conf`
- **Windows**: `%APPDATA%\ngpt\ngpt.conf`

The configuration file uses a JSON list format, allowing you to store multiple configurations. You can select which configuration to use with the `--config-index` argument (or by default, index 0 is used).

#### Multiple Configurations Example (`ngpt.conf`)
```json
[
  {
    "api_key": "your-openai-api-key-here",
    "base_url": "https://api.openai.com/v1/",
    "provider": "OpenAI",
    "model": "gpt-4o"
  },
  {
    "api_key": "your-groq-api-key-here",
    "base_url": "https://api.groq.com/openai/v1/",
    "provider": "Groq",
    "model": "llama3-70b-8192"
  },
  {
    "api_key": "your-ollama-key-if-needed",
    "base_url": "http://localhost:11434/v1/",
    "provider": "Ollama-Local",
    "model": "llama3"
  }
]
```

### Configuration Priority

nGPT determines configuration values in the following order (highest priority first):

1. Command line arguments (`--api-key`, `--base-url`, `--model`)
2. Environment variables (`OPENAI_API_KEY`, `OPENAI_BASE_URL`, `OPENAI_MODEL`)
3. Configuration file (selected by `--config-index`, defaults to index 0)
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