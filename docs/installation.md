# Installation Guide

There are several ways to install nGPT depending on your needs and environment.

## Requirements

- Python 3.8 or newer
- `requests` library (automatically installed as a dependency)
- `prompt_toolkit` library (automatically installed as a dependency)

## Optional Dependencies

- `rich` library - For enhanced markdown rendering with syntax highlighting

## Installing from PyPI (Recommended)

The simplest way to install nGPT is through the Python Package Index (PyPI):

```bash
pip install ngpt
```

This will install the latest stable release of nGPT and all its dependencies.

For markdown rendering capabilities, install with the prettify extra:

```bash
pip install ngpt[prettify]
```

Alternatively, you can install the optional dependency separately:

```bash
pip install rich
```

## Installing in a Virtual Environment

It's often good practice to install Python packages in a virtual environment to avoid conflicts:

### Using venv

```bash
# Create a virtual environment
python -m venv ngpt-env

# Activate the environment
# On Windows:
ngpt-env\Scripts\activate
# On macOS and Linux:
source ngpt-env/bin/activate

# Install nGPT
pip install ngpt
```

### Using conda

```bash
# Create a conda environment
conda create -n ngpt-env python=3.10

# Activate the environment
conda activate ngpt-env

# Install nGPT
pip install ngpt
```

## Installing from Source

To install the latest development version from source:

```bash
# Clone the repository
git clone https://github.com/nazdridoy/ngpt.git

# Navigate to the project directory
cd ngpt

# Install the package in development mode
pip install -e .
```

## Upgrading

To upgrade to the latest version:

```bash
pip install --upgrade ngpt
```

## Verifying the Installation

After installation, you can verify that nGPT is installed correctly by checking the version:

```bash
ngpt --version
```

You should see the version number of nGPT displayed.

## Next Steps

After installation, you can:
- Configure your API keys and preferences using `ngpt --config`
- Start using the CLI tool with `ngpt "Your prompt here"`
- Import the library in your Python projects: `from ngpt import NGPTClient`

For more information, see the [Library Usage](usage/library_usage.md) and [CLI Usage](usage/cli_usage.md) guides. 