# NGPTClient

`NGPTClient` is the primary class for interacting with OpenAI-compatible APIs. It provides methods for chat completion, code generation, shell command generation, and model listing.

## Initialization

```python
from ngpt import NGPTClient

client = NGPTClient(
    api_key: str = "",
    base_url: str = "https://api.openai.com/v1/",
    provider: str = "OpenAI",
    model: str = "gpt-3.5-turbo"
)
```

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `api_key` | `str` | `""` | API key for authentication |
| `base_url` | `str` | `"https://api.openai.com/v1/"` | Base URL for the API endpoint |
| `provider` | `str` | `"OpenAI"` | Name of the provider (for reference only) |
| `model` | `str` | `"gpt-3.5-turbo"` | Default model to use for completion |

### Examples

```python
# Basic initialization with OpenAI
client = NGPTClient(api_key="your-openai-api-key")

# Using a different provider
client = NGPTClient(
    api_key="your-api-key",
    base_url="https://api.groq.com/openai/v1/",
    provider="Groq",
    model="llama3-70b-8192"
)

# Using a local Ollama instance
client = NGPTClient(
    api_key="",  # No key needed for local Ollama
    base_url="http://localhost:11434/v1/",
    provider="Ollama-Local",
    model="llama3"
)
```

## Chat Method

The primary method for interacting with the AI model.

```python
response = client.chat(
    prompt: str,
    stream: bool = True,
    temperature: float = 0.7,
    max_tokens: Optional[int] = None,
    messages: Optional[List[Dict[str, str]]] = None,
    web_search: bool = False,
    **kwargs
) -> str
```

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `prompt` | `str` | Required | The user's message |
| `stream` | `bool` | `True` | Whether to stream the response |
| `temperature` | `float` | `0.7` | Controls randomness in the response (0.0-1.0) |
| `max_tokens` | `Optional[int]` | `None` | Maximum number of tokens to generate |
| `messages` | `Optional[List[Dict[str, str]]]` | `None` | Optional list of message objects for conversation history |
| `web_search` | `bool` | `False` | Whether to enable web search capability |
| `**kwargs` | | | Additional arguments to pass to the API |

### Returns

- When `stream=False`: A string containing the complete response
- When `stream=True`: A generator yielding response chunks that can be iterated over

### Examples

```python
# Basic chat with streaming
for chunk in client.chat("Tell me about quantum computing"):
    print(chunk, end="", flush=True)
print()  # Final newline

# Without streaming
response = client.chat("Tell me about quantum computing", stream=False)
print(response)

# With conversation history
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Hello, who are you?"},
    {"role": "assistant", "content": "I'm an AI assistant. How can I help you today?"},
    {"role": "user", "content": "Tell me about yourself"}
]
response = client.chat("", messages=messages)
print(response)

# With web search
response = client.chat("What's the latest news about AI?", web_search=True)
print(response)

# With temperature control
response = client.chat("Write a creative story", temperature=0.9)  # More random
response = client.chat("Explain how a CPU works", temperature=0.2)  # More focused

# With token limit
response = client.chat("Summarize this concept", max_tokens=100)
```

## Generate Shell Command

Generates a shell command based on the prompt, optimized for the user's operating system.

```python
command = client.generate_shell_command(
    prompt: str,
    web_search: bool = False
) -> str
```

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `prompt` | `str` | Required | Description of the command to generate |
| `web_search` | `bool` | `False` | Whether to enable web search capability |

### Returns

A string containing the generated shell command appropriate for the user's OS.

### Examples

```python
# Generate a command to find large files
command = client.generate_shell_command("find all files larger than 100MB")
print(f"Generated command: {command}")

# Execute the generated command
import subprocess
result = subprocess.run(command, shell=True, capture_output=True, text=True)
print(f"Output: {result.stdout}")

# With web search for more current command syntax
command = client.generate_shell_command(
    "show Docker container resource usage in a nice format",
    web_search=True
)
```

## Generate Code

Generates clean code based on the prompt, without markdown formatting or explanations.

```python
code = client.generate_code(
    prompt: str,
    language: str = "python",
    web_search: bool = False
) -> str
```

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `prompt` | `str` | Required | Description of the code to generate |
| `language` | `str` | `"python"` | Programming language to generate code in |
| `web_search` | `bool` | `False` | Whether to enable web search capability |

### Returns

A string containing the generated code without any markdown formatting or explanations.

### Examples

```python
# Generate Python code (default)
python_code = client.generate_code("function to calculate fibonacci numbers")
print(python_code)

# Generate JavaScript code
js_code = client.generate_code(
    "function to validate email addresses using regex",
    language="javascript"
)
print(js_code)

# Generate code with web search for latest best practices
react_code = client.generate_code(
    "create a React component that fetches and displays data from an API",
    language="jsx",
    web_search=True
)
```

## List Models

Retrieves the list of available models from the API.

```python
models = client.list_models() -> list
```

### Returns

A list of available model objects or an empty list if the request failed.

### Examples

```python
# Get available models
models = client.list_models()

# Print model IDs
if models:
    print("Available models:")
    for model in models:
        print(f"- {model.get('id')}")
else:
    print("No models available or could not retrieve models")

# Filter for specific models
gpt4_models = [m for m in models if "gpt-4" in m.get('id', '')]
for model in gpt4_models:
    print(f"GPT-4 model: {model.get('id')}")
```

## Error Handling

The `NGPTClient` methods include basic error handling for common issues:

- HTTP errors (401, 404, 429, etc.)
- Connection errors
- Timeout errors
- JSON parsing errors

For production code, it's recommended to implement your own error handling:

```python
import requests

try:
    response = client.chat("Tell me about quantum computing")
except requests.exceptions.HTTPError as e:
    if e.response.status_code == 401:
        print("Authentication failed. Check your API key.")
    elif e.response.status_code == 429:
        print("Rate limit exceeded. Please wait and try again.")
    else:
        print(f"HTTP error: {e}")
except requests.exceptions.ConnectionError:
    print("Connection error. Check your internet and base URL.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
``` 