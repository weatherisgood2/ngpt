# Library Usage Guide

This guide provides comprehensive documentation on how to use nGPT as a Python library in your applications.

## Installation

First, ensure you have nGPT installed:

```bash
pip install ngpt
```

## Basic Usage

### Importing the Library

The main components you'll need are the `NGPTClient` class and configuration utilities:

```python
from ngpt import NGPTClient, load_config
```

### Initializing the Client

You can initialize the client in several ways:

#### Using Configuration Files

```python
# Load default configuration (index 0)
config = load_config()
client = NGPTClient(**config)

# Or specify a different configuration
config = load_config(config_index=1)
client = NGPTClient(**config)
```

#### Direct Initialization

```python
client = NGPTClient(
    api_key="your-api-key",
    base_url="https://api.openai.com/v1/",
    provider="OpenAI",  # Optional, for reference only
    model="gpt-4o"
)
```

### Basic Chat

The most basic functionality is sending a chat message:

```python
response = client.chat("Tell me about quantum computing")
print(response)
```

## Advanced Usage

### Streaming Responses

For real-time streaming of responses:

```python
for chunk in client.chat("Write a poem about Python", stream=True):
    print(chunk, end="", flush=True)
print()  # Final newline
```

### Conversation History

To maintain a conversation with context:

```python
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Hello, who are you?"}
]

response = client.chat("", messages=messages)
print(response)

# Update messages for the next turn
messages.append({"role": "assistant", "content": response})
messages.append({"role": "user", "content": "Tell me more about yourself"})

response = client.chat("", messages=messages)
print(response)
```

### Generating Shell Commands

Generate OS-aware shell commands:

```python
command = client.generate_shell_command("find all python files modified in the last week")
print(f"Generated command: {command}")

# Optionally execute the command
import subprocess
result = subprocess.run(command, shell=True, capture_output=True, text=True)
print(f"Output: {result.stdout}")
```

### Generating Code

Generate clean code without markdown or explanations:

```python
code = client.generate_code("function that sorts a list using quicksort algorithm")
print(code)

# Specify a different language
javascript_code = client.generate_code("function to calculate Fibonacci sequence", language="javascript")
print(javascript_code)
```

### Web Search Capability

If your API endpoint supports it, you can enable web search:

```python
response = client.chat("What are the latest developments in quantum computing?", web_search=True)
print(response)
```

### Listing Available Models

List models available through your API endpoint:

```python
models = client.list_models()
for model in models:
    print(f"ID: {model.get('id')}")
```

## Configuration Management

### Working with Configuration Files

```python
from ngpt.config import (
    load_config, 
    load_configs, 
    get_config_path, 
    get_config_dir,
    create_default_config,
    add_config_entry,
    remove_config_entry
)

# Get config directory path
config_dir = get_config_dir()
print(f"Config directory: {config_dir}")

# Get config file path
config_path = get_config_path()
print(f"Config file: {config_path}")

# Load all configurations
configs = load_configs()
print(f"Found {len(configs)} configurations")

# Load a specific configuration
config = load_config(config_index=0)
print(f"Using provider: {config.get('provider', 'Unknown')}")
```

### Using Multiple API Endpoints

Switch between different API providers:

```python
# Load configurations for different providers
openai_config = load_config(config_index=0)  # OpenAI config
groq_config = load_config(config_index=1)    # Groq config
ollama_config = load_config(config_index=2)  # Ollama config

# Create clients for each provider
openai_client = NGPTClient(**openai_config)
groq_client = NGPTClient(**groq_config)
ollama_client = NGPTClient(**ollama_config)

# Use each client
openai_response = openai_client.chat("Hello from OpenAI")
groq_response = groq_client.chat("Hello from Groq")
ollama_response = ollama_client.chat("Hello from Ollama")
```

## Complete Examples

### Simple Chat Bot

```python
from ngpt import NGPTClient, load_config

def simple_chat_bot():
    # Initialize client with default configuration
    config = load_config()
    client = NGPTClient(**config)
    
    print("Simple Chat Bot (type 'exit' to quit)")
    print("-" * 50)
    
    while True:
        user_input = input("You: ")
        if user_input.lower() in ['exit', 'quit', 'bye']:
            break
            
        print("Bot: ", end="", flush=True)
        response = ""
        for chunk in client.chat(user_input, stream=True):
            print(chunk, end="", flush=True)
            response += chunk
        print()  # Final newline
    
    print("Goodbye!")

if __name__ == "__main__":
    simple_chat_bot()
```

### Code Generation Utility

```python
from ngpt import NGPTClient, load_config
import argparse
import sys

def code_generator():
    parser = argparse.ArgumentParser(description="Generate code using nGPT")
    parser.add_argument("prompt", help="Description of the code to generate")
    parser.add_argument("--language", "-l", default="python", help="Programming language (default: python)")
    parser.add_argument("--output", "-o", help="Output file (default: print to stdout)")
    args = parser.parse_args()
    
    # Initialize client
    config = load_config()
    client = NGPTClient(**config)
    
    # Generate code
    try:
        code = client.generate_code(args.prompt, language=args.language)
        
        if args.output:
            with open(args.output, 'w') as f:
                f.write(code)
            print(f"Code written to {args.output}")
        else:
            print(code)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    code_generator()
```

### Web Search Assistant

```python
from ngpt import NGPTClient, load_config

def web_search_assistant():
    # Initialize client with default configuration
    config = load_config()
    client = NGPTClient(**config)
    
    print("Web Search Assistant (type 'exit' to quit)")
    print("-" * 50)
    print("Ask me anything that requires current information!")
    
    while True:
        user_input = input("Question: ")
        if user_input.lower() in ['exit', 'quit', 'bye']:
            break
            
        print("Searching and generating response...")
        response = client.chat(user_input, web_search=True)
        print("\nAnswer:")
        print(response)
        print("-" * 50)
    
    print("Goodbye!")

if __name__ == "__main__":
    web_search_assistant()
```

## Error Handling

The client provides basic error handling, but you should implement your own error handling for production code:

```python
from ngpt import NGPTClient
import requests

client = NGPTClient(api_key="your-api-key")

try:
    response = client.chat("Tell me about quantum computing")
    print(response)
except requests.exceptions.HTTPError as e:
    print(f"HTTP Error: {e}")
except requests.exceptions.ConnectionError:
    print("Connection Error: Could not connect to the API endpoint")
except requests.exceptions.Timeout:
    print("Timeout Error: The request timed out")
except requests.exceptions.RequestException as e:
    print(f"Request Error: {e}")
except Exception as e:
    print(f"Unexpected Error: {e}")
```

## Next Steps

- Check out the [API Reference](../api/README.md) for detailed information on all available functions and classes
- Explore the [Examples](../examples/README.md) section for more usage examples
- See the [Configuration Guide](../configuration.md) for advanced configuration options 