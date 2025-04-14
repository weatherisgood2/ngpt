# tOAI

A lightweight Python CLI and library for interacting with custom OpenAI API endpoints.

## Features

- Dual mode: Use as a CLI tool or import as a library
- Minimal dependencies
- Customizable API endpoints and providers
- Streaming responses
- Web search capability (supported by compatible API endpoints)
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
# Basic chat
tOAI chat "Hello, how are you?"

# With custom options
tOAI --api-key your-key --base-url http://your-endpoint chat "Hello"

# Enable web search (if your API endpoint supports it)
tOAI --web-search chat "What's the latest news about AI?"

# Generate and execute shell commands
tOAI shell "list all files in current directory"

# Generate code
tOAI code "create a python function that calculates fibonacci numbers"
```

### As a Library

```python
from tOAI import TOAIClient

# Initialize the client
client = TOAIClient(
    api_key="your-key",
    base_url="http://your-endpoint",
    provider="openai",
    model="Claude-sonnet-3.7"
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

You can configure the client using the following options:

- `--api-key`: API key for the service
- `--base-url`: Base URL for the API
- `--provider`: Provider name
- `--model`: Model to use
- `--web-search`: Enable web search capability (Note: Your API endpoint must support this feature)

## Environment Variables

The following environment variables can be set in a `.env` file:

```
OPENAI_API_KEY=your_api_key_here
OPENAI_BASE_URL=http://127.0.0.1:1337/v1/
OPENAI_PROVIDER=Blackbox
OPENAI_MODEL=Claude-sonnet-3.7
```

## Special Features

### OS-Aware Shell Commands

Shell command generation is OS-aware, providing appropriate commands for your operating system (Windows, macOS, or Linux) and shell type (bash, powershell, etc.).

### Clean Code Generation

Code generation uses an improved prompt that ensures only clean code is returned, without markdown formatting or unnecessary explanations.

## Implementation Notes

This library uses direct HTTP requests instead of the OpenAI client library, allowing it to work with custom API endpoints that support additional parameters like `provider` and `web_search`. All parameters are sent directly in the request body, similar to the format shown in the curl example.

## License

MIT 