# nGPT

[![PyPI version](https://img.shields.io/pypi/v/ngpt.svg)](https://pypi.org/project/ngpt/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Versions](https://img.shields.io/pypi/pyversions/ngpt.svg)](https://pypi.org/project/ngpt/)

A lightweight Python CLI and library for interacting with OpenAI-compatible APIs, supporting both official and self-hosted LLM endpoints.

## Table of Contents
- [Quick Start](#quick-start)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
  - [CLI Tool](#as-a-cli-tool)
  - [Python Library](#as-a-library)
- [Configuration](#configuration)
  - [Command Line Options](#command-line-options)
  - [Configuration File](#configuration-file)
  - [Configuration Priority](#configuration-priority)
- [Contributing](#contributing)
- [License](#license)

## Quick Start

```bash
# Install
pip install ngpt

# Chat with default settings
ngpt "Tell me about quantum computing"

# Generate code
ngpt --code "function to calculate the Fibonacci sequence"

# Generate and execute shell commands
ngpt --shell "list all files in the current directory"
```

## Features

- ✅ **Dual Mode**: Use as a CLI tool or import as a Python library
- 🪶 **Lightweight**: Minimal dependencies (just `requests`)
- 🔄 **API Flexibility**: Works with OpenAI, Ollama, Groq, and any compatible endpoint
- 📊 **Streaming Responses**: Real-time output for better user experience
- 🔍 **Web Search**: Integrated with compatible API endpoints
- ⚙️ **Multiple Configurations**: Cross-platform config system supporting different profiles
- 💻 **Shell Command Generation**: OS-aware command execution
- 🧩 **Clean Code Generation**: Output code without markdown or explanations

## Installation

```bash
pip install ngpt
```

Requires Python 3.8 or newer.

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
ngpt --api-key your-key --base-url http://your-endpoint --model your-model "Hello"

# Enable web search (if your API endpoint supports it)
ngpt --web-search "What's the latest news about AI?"

# Generate and execute shell commands (using -s or --shell flag)
# OS-aware: generates appropriate commands for Windows, macOS, or Linux
ngpt -s "list all files in current directory"
# On Windows generates: dir
# On Linux/macOS generates: ls -la

# Generate clean code (using -c or --code flag)
# Returns only code without markdown formatting or explanations
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

#### Advanced Library Usage

```python
# Stream responses
for chunk in client.chat("Write a poem about Python", stream=True):
    print(chunk, end="", flush=True)

# Customize system prompt
response = client.chat(
    "Explain quantum computing",
    system_prompt="You are a quantum physics professor. Explain complex concepts simply."
)

# OS-aware shell commands
# Automatically generates appropriate commands for the current OS
command = client.generate_shell_command("find large files")
import subprocess
result = subprocess.run(command, shell=True, capture_output=True, text=True)
print(result.stdout)

# Clean code generation
# Returns only code without markdown or explanations
code = client.generate_code("function that converts Celsius to Fahrenheit")
print(code)
```

## Configuration

### Command Line Options

You can configure the client using the following options:

| Option | Description |
|--------|-------------|
| `--api-key` | API key for the service |
| `--base-url` | Base URL for the API |
| `--model` | Model to use |
| `--web-search` | Enable web search capability |
| `--config` | Path to a custom configuration file |
| `--config-index` | Index of the configuration to use (default: 0) |
| `--show-config` | Show configuration details and exit |
| `--all` | Used with `--show-config` to display all configurations |
| `-s, --shell` | Generate and execute shell commands |
| `-c, --code` | Generate clean code output |
| `-v, --version` | Show version information |

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

## Contributing

We welcome contributions to nGPT! Whether it's bug fixes, feature additions, or documentation improvements, your help is appreciated.

To contribute:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Make your changes
4. Commit with clear messages following conventional commit guidelines
5. Push to your fork and submit a pull request

Please check the [CONTRIBUTING.md](CONTRIBUTING.md) file for detailed guidelines on code style, pull request process, and development setup.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.