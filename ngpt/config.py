import os
import sys
import json
from pathlib import Path
from typing import Dict, Optional, Any, List

# Default configuration
DEFAULT_CONFIG_ENTRY = {
    "api_key": "",
    "base_url": "https://api.openai.com/v1/",
    "provider": "OpenAI",
    "model": "gpt-3.5-turbo"
}

# Default configurations list
DEFAULT_CONFIG = [DEFAULT_CONFIG_ENTRY]

def get_config_dir() -> Path:
    """Get the appropriate config directory based on OS."""
    if sys.platform == "win32":
        # Windows
        config_dir = Path(os.environ.get("APPDATA", "")) / "ngpt"
    elif sys.platform == "darwin":
        # macOS
        config_dir = Path.home() / "Library" / "Application Support" / "ngpt"
    else:
        # Linux and other Unix-like systems
        xdg_config_home = os.environ.get("XDG_CONFIG_HOME")
        if xdg_config_home:
            config_dir = Path(xdg_config_home) / "ngpt"
        else:
            config_dir = Path.home() / ".config" / "ngpt"
    
    # Ensure the directory exists
    config_dir.mkdir(parents=True, exist_ok=True)
    return config_dir

def get_config_path(custom_path: Optional[str] = None) -> Path:
    """Get the path to the config file."""
    if custom_path:
        return Path(custom_path)
    return get_config_dir() / "ngpt.conf"

def create_default_config(config_path: Path) -> None:
    """Create a default configuration file with a single config entry."""
    with open(config_path, "w") as f:
        json.dump(DEFAULT_CONFIG, f, indent=2)
    print(f"Created default configuration file at {config_path}")

def add_config_entry(config_path: Path, config_index: Optional[int] = None) -> None:
    """Add a new configuration entry or update existing one at the specified index."""
    configs = load_configs(custom_path=str(config_path))
    
    # Create a new entry based on the default
    new_entry = DEFAULT_CONFIG_ENTRY.copy()
    
    # Interactive configuration
    print("Enter configuration details (press Enter to use default values):")
    new_entry["api_key"] = input(f"API Key: ") or new_entry["api_key"]
    new_entry["base_url"] = input(f"Base URL [{new_entry['base_url']}]: ") or new_entry["base_url"]
    new_entry["provider"] = input(f"Provider [{new_entry['provider']}]: ") or new_entry["provider"]
    new_entry["model"] = input(f"Model [{new_entry['model']}]: ") or new_entry["model"]
    
    # Add or update the entry
    if config_index is not None and config_index < len(configs):
        configs[config_index] = new_entry
        print(f"Updated configuration at index {config_index}")
    else:
        configs.append(new_entry)
        print(f"Added new configuration at index {len(configs)-1}")
    
    # Save the updated configs
    with open(config_path, "w") as f:
        json.dump(configs, f, indent=2)

def load_configs(custom_path: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Load all configurations from the config file.
    Returns a list of configuration dictionaries.
    """
    config_path = get_config_path(custom_path)
    
    # Start with default configs
    configs = DEFAULT_CONFIG.copy()
    
    # Load from config file if it exists
    if config_path.exists():
        try:
            with open(config_path, "r") as f:
                file_configs = json.load(f)
                # Handle both old format (single dict) and new format (list of dicts)
                if isinstance(file_configs, dict):
                    # Convert old format to new format
                    configs = [file_configs]
                else:
                    configs = file_configs
        except (json.JSONDecodeError, IOError) as e:
            print(f"Warning: Could not read config file: {e}", file=sys.stderr)
    else:
        # Create default config file if it doesn't exist
        create_default_config(config_path)
    
    return configs

def load_config(custom_path: Optional[str] = None, config_index: int = 0) -> Dict[str, Any]:
    """
    Load a specific configuration by index and apply environment variables.
    Environment variables take precedence over the config file.
    """
    configs = load_configs(custom_path)
    
    # If config_index is out of range, use the first config
    if config_index < 0 or config_index >= len(configs):
        if len(configs) > 0:
            config_index = 0
            print(f"Warning: Config index {config_index} is out of range. Using index 0 instead.")
        else:
            # This should not happen as load_configs should always return at least DEFAULT_CONFIG
            return DEFAULT_CONFIG_ENTRY.copy()
    
    # Get the selected config
    config = configs[config_index]
    
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