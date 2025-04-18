# Usage Guide

This section contains comprehensive documentation on how to use nGPT, both as a command-line interface (CLI) tool and as a Python library.

## Table of Contents

- [Library Usage](library_usage.md) - Learn how to integrate nGPT into your Python projects
- [CLI Usage](cli_usage.md) - Learn how to use nGPT from the command line

## Overview

nGPT offers two primary ways to use it:

### 1. Command-Line Interface (CLI)

nGPT provides a powerful and intuitive command-line interface that allows you to:

- Chat with AI models using simple commands
- Conduct interactive chat sessions with conversation memory
- Generate and execute shell commands
- Generate clean code without markdown formatting
- Configure API settings and preferences
- And more...

See the [CLI Usage](cli_usage.md) guide for detailed documentation.

### 2. Python Library

nGPT can be imported as a Python library, allowing you to:

- Integrate AI capabilities into your Python applications
- Chat with AI models programmatically
- Generate code and shell commands
- Stream responses in real-time
- Use multiple configurations for different providers
- And more...

See the [Library Usage](library_usage.md) guide for detailed documentation and examples.

## Quick Reference

### CLI Quick Start

```bash
# Basic chat
ngpt "Tell me about quantum computing"

# Interactive chat session
ngpt -i

# Generate shell command
ngpt --shell "list all PDF files recursively"

# Generate code
ngpt --code "function to calculate prime numbers"
```

### Library Quick Start

```python
from ngpt import NGPTClient, load_config

# Load configuration
config = load_config()

# Initialize client
client = NGPTClient(**config)

# Chat with AI
response = client.chat("Tell me about quantum computing")
print(response)

# Generate code
code = client.generate_code("function to calculate prime numbers")
print(code)

# Generate shell command
command = client.generate_shell_command("list all PDF files recursively")
print(command)
```

For more detailed information, see the specific usage guides. 