import os
import sys
import json
from pathlib import Path
from typing import Dict, Optional, Any

# Default configuration
DEFAULT_CONFIG = {
    "api_key": "",
    "base_url": "https://api.openai.com/v1/",
    "provider": "OpenAI",
    "model": "gpt-3.5-turbo"
}

def get_config_dir() -> Path:
    """Get the appropriate config directory based on OS."""
    if sys.platform == "win32":
        # Windows
        config_dir = Path(os.environ.get("APPDATA", "")) / "tOAI"
    elif sys.platform == "darwin":
        # macOS
        config_dir = Path.home() / "Library" / "Application Support" / "tOAI"
    else:
        # Linux and other Unix-like systems
        xdg_config_home = os.environ.get("XDG_CONFIG_HOME")
        if xdg_config_home:
            config_dir = Path(xdg_config_home) / "tOAI"
        else:
            config_dir = Path.home() / ".config" / "tOAI"
    
    # Ensure the directory exists
    config_dir.mkdir(parents=True, exist_ok=True)
    return config_dir

def get_config_path(custom_path: Optional[str] = None) -> Path:
    """Get the path to the config file."""
    if custom_path:
        return Path(custom_path)
    return get_config_dir() / "tOAI.conf"

def create_default_config(config_path: Path) -> None:
    """Create a default configuration file."""
    with open(config_path, "w") as f:
        json.dump(DEFAULT_CONFIG, f, indent=2)
    print(f"Created default configuration file at {config_path}")

def load_config(custom_path: Optional[str] = None) -> Dict[str, Any]:
    """
    Load configuration from file and environment variables.
    Environment variables take precedence over the config file.
    """
    config_path = get_config_path(custom_path)
    
    # Start with default config
    config = DEFAULT_CONFIG.copy()
    
    # Load from config file if it exists
    if config_path.exists():
        try:
            with open(config_path, "r") as f:
                file_config = json.load(f)
                config.update(file_config)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Warning: Could not read config file: {e}", file=sys.stderr)
    else:
        # Create default config file if it doesn't exist
        create_default_config(config_path)
    
    # Override with environment variables if they exist
    env_mapping = {
        "OPENAI_API_KEY": "api_key",
        "OPENAI_BASE_URL": "base_url",
        "OPENAI_PROVIDER": "provider", 
        "OPENAI_MODEL": "model"
    }
    
    for env_var, config_key in env_mapping.items():
        if env_var in os.environ and os.environ[env_var]:
            config[config_key] = os.environ[env_var]
    
    return config 