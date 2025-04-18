# CLI Usage Guide

This guide provides comprehensive documentation on how to use nGPT as a command-line interface (CLI) tool.

## Installation

First, ensure you have nGPT installed:

```bash
pip install ngpt
```

## Basic Usage

The most basic way to use nGPT from the command line is to provide a prompt:

```bash
ngpt "Tell me about quantum computing"
```

This will send your prompt to the configured AI model and stream the response to your terminal.

## Command Overview

```bash
ngpt [OPTIONS] [PROMPT]
```

Where:
- `[OPTIONS]` are command-line flags that modify behavior
- `[PROMPT]` is your text prompt to the AI (optional with certain flags)

## Common Options

Here are the most commonly used options:

| Option | Description |
|--------|-------------|
| `-i, --interactive` | Start an interactive chat session with conversation memory |
| `-n, --no-stream` | Return the whole response without streaming |
| `-s, --shell` | Generate and execute shell commands |
| `-c, --code` | Generate clean code without markdown formatting |
| `-t, --text` | Open interactive multiline editor for complex prompts |
| `-v, --version` | Show version information |
| `--web-search` | Enable web search capability (if supported by your API) |

## Feature Details

### Basic Chat

Send a simple prompt and get a response:

```bash
ngpt "What is the capital of France?"
```

The response will be streamed in real-time to your terminal.

### Interactive Chat

Start an interactive chat session with conversation memory:

```bash
ngpt -i
```

This opens a continuous chat session where the AI remembers previous exchanges. In interactive mode:

- Type your messages and press Enter to send
- Use arrow keys to navigate message history
- Press Ctrl+C to exit the session

### Generating Shell Commands

Generate and execute shell commands appropriate for your operating system:

```bash
ngpt -s "find all PDF files in the current directory"
```

nGPT will generate an appropriate command based on your operating system, display it, and ask for confirmation before executing it.

### Generating Code

Generate clean code without markdown or explanations:

```bash
ngpt -c "function that calculates the Fibonacci sequence"
```

This returns only the code, without any surrounding markdown formatting or explanations.

### Multiline Text Input

Open an interactive editor for entering complex, multiline prompts:

```bash
ngpt -t
```

This opens an editor where you can:
- Write and edit multiline text
- Press Ctrl+D or F10 to submit the text
- Press Esc to cancel

### Using Web Search

Enable web search capability (if your API endpoint supports it):

```bash
ngpt --web-search "What are the latest developments in quantum computing?"
```

This allows the AI to access current information from the web when generating a response.

## Configuration Options

### Viewing Current Configuration

Show your current active configuration:

```bash
ngpt --show-config
```

Show all stored configurations:

```bash
ngpt --show-config --all
```

### Setting Configuration Options

Select a specific configuration by index:

```bash
ngpt --config-index 1 "Your prompt here"
```

Specify API credentials directly:

```bash
ngpt --api-key "your-key" --base-url "https://api.example.com/v1/" --model "model-name" "Your prompt here"
```

### Interactive Configuration

Add a new configuration interactively:

```bash
ngpt --config
```

Edit an existing configuration:

```bash
ngpt --config --config-index 1
```

Remove a configuration:

```bash
ngpt --config --remove --config-index 2
```

### Model Management

List all available models for the current configuration:

```bash
ngpt --list-models
```

List models for a specific configuration:

```bash
ngpt --list-models --config-index 1
```

## Advanced Usage

### Combining Options

You can combine various options:

```bash
# Generate code with web search capability
ngpt -c --web-search "function to get current weather using an API"

# Use a specific model and no streaming
ngpt --model gpt-4o-mini -n "Explain quantum entanglement"
```

### Using a Custom Configuration File

Specify a custom configuration file location:

```bash
ngpt --config /path/to/custom-config.json "Your prompt here"
```

### Setting Temperature

Control the randomness of responses:

```bash
# More deterministic responses
ngpt --temperature 0.2 "Write a poem about autumn"

# More creative responses
ngpt --temperature 0.9 "Write a poem about autumn"
```

## Examples by Task

### Creative Writing

```bash
# Generate a short story
ngpt "Write a 300-word sci-fi story about time travel"

# Write poetry
ngpt "Write a haiku about mountains"
```

### Programming Help

```bash
# Get programming help
ngpt "How do I read a file line by line in Python?"

# Generate code
ngpt -c "create a function that validates email addresses using regex"
```

### Research and Learning

```bash
# Learn about a topic
ngpt "Explain quantum computing for beginners"

# Get current information (with web search)
ngpt --web-search "What are the latest advancements in AI?"
```

### Productivity

```bash
# Generate a shell command
ngpt -s "find large files over 100MB and list them by size"

# Create a structured document
ngpt -t
# (Enter multiline text for generating a complex document)
```

## Troubleshooting

### API Connection Issues

If you're having trouble connecting to the API:

```bash
# Check your current configuration
ngpt --show-config

# Try specifying the base URL directly
ngpt --base-url "https://api.example.com/v1/" "Test connection"
```

### Authorization Problems

If you're experiencing authentication issues:

```bash
# Update your API key
ngpt --config --config-index 0
# Enter your new API key when prompted

# Or specify API key directly (not recommended for sensitive keys)
ngpt --api-key "your-new-api-key" "Test prompt"
```

### Command Not Found

If the `ngpt` command is not found after installation:

- Ensure Python's bin directory is in your PATH
- Try using `python -m ngpt` instead of just `ngpt`

## Tips and Best Practices

1. **Use the right tool for the job**:
   - Use `-c` for clean code generation
   - Use `-s` for shell commands
   - Use `-t` for complex, multiline inputs

2. **Craft effective prompts**:
   - Be specific about what you want
   - Provide context and examples when relevant
   - Specify format, style, or constraints

3. **Leverage configuration profiles**:
   - Set up different profiles for different API providers
   - Use lower-cost models for simpler tasks
   - Reserve more powerful models for complex tasks

4. **Protect API keys**:
   - Store API keys in your configuration file
   - Avoid passing API keys directly on the command line
   - Use environment variables when appropriate

5. **Improve efficiency**:
   - Use `-n` (no streaming) for faster responses in scripts
   - Use interactive mode when having a conversation
   - Exit interactive sessions when not in use to save API costs 