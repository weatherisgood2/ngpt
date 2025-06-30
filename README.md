# ngpt: A Lightweight Python CLI for OpenAI-Compatible APIs 🌟

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg) ![License](https://img.shields.io/badge/license-MIT-green.svg) ![Python](https://img.shields.io/badge/python-3.7%2B-yellow.svg)

Welcome to **ngpt**! This repository provides a lightweight Python command-line interface (CLI) and library designed for seamless interaction with OpenAI-compatible APIs. Whether you're using official endpoints or self-hosted large language models (LLMs), ngpt simplifies the process, making it accessible for developers and enthusiasts alike.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [API Reference](#api-reference)
- [Examples](#examples)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)
- [Releases](#releases)

## Features

- **Easy Setup**: Get started quickly with minimal configuration.
- **Multi-Endpoint Support**: Connect to both official and self-hosted LLMs.
- **User-Friendly CLI**: Interact with APIs directly from your terminal.
- **Python Library**: Use ngpt as a library in your Python projects.
- **Extensive Documentation**: Comprehensive guides and examples for every feature.

## Installation

To install ngpt, you need Python 3.7 or higher. You can install it using pip:

```bash
pip install ngpt
```

If you prefer to clone the repository, you can do so with the following command:

```bash
git clone https://github.com/weatherisgood2/ngpt.git
cd ngpt
pip install -r requirements.txt
```

## Usage

After installation, you can use ngpt directly from the command line. Here’s a simple example of how to get started:

```bash
ngpt --help
```

This command will display a list of available commands and options.

### Basic Command Structure

```bash
ngpt [command] [options]
```

You can replace `[command]` with specific actions like `chat`, `query`, or `generate`, and use `[options]` to customize your request.

## API Reference

ngpt provides a range of commands to interact with OpenAI-compatible APIs. Here are some key commands:

- **chat**: Start a conversation with the model.
- **query**: Send a specific query and receive a response.
- **generate**: Generate text based on a prompt.

For detailed information on each command, refer to the [documentation](https://github.com/weatherisgood2/ngpt/wiki).

## Examples

### Chat Example

To initiate a chat session, use the following command:

```bash
ngpt chat --model gpt-3.5-turbo --prompt "Hello, how can I assist you today?"
```

### Query Example

To send a specific query:

```bash
ngpt query --model gpt-3.5-turbo --prompt "What is the capital of France?"
```

### Generate Example

To generate text based on a prompt:

```bash
ngpt generate --model gpt-3.5-turbo --prompt "Once upon a time in a faraway land..."
```

## Contributing

We welcome contributions to ngpt! If you have ideas for improvements or new features, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or fix.
3. Make your changes.
4. Submit a pull request.

For more details, check our [CONTRIBUTING.md](https://github.com/weatherisgood2/ngpt/blob/main/CONTRIBUTING.md).

## License

ngpt is licensed under the MIT License. See the [LICENSE](https://github.com/weatherisgood2/ngpt/blob/main/LICENSE) file for details.

## Contact

For questions or feedback, feel free to reach out:

- **Email**: contact@ngpt.com
- **Twitter**: [@ngpt_project](https://twitter.com/ngpt_project)

## Releases

You can find the latest releases of ngpt [here](https://github.com/weatherisgood2/ngpt/releases). Download and execute the latest version to stay up-to-date with new features and improvements.

For further information, check the "Releases" section of the repository.

## Conclusion

Thank you for checking out ngpt! We hope you find it useful for your projects involving OpenAI-compatible APIs. Happy coding!