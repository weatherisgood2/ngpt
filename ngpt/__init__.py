try:
    from importlib.metadata import version as get_version
    __version__ = get_version("ngpt")
except ImportError:
    # For Python < 3.8 or package not installed
    __version__ = "1.0.0"  # fallback version

from .client import NGPTClient
from .config import load_config, get_config_path, get_config_dir

__all__ = ["NGPTClient", "__version__", "load_config", "get_config_path", "get_config_dir"]

# Import cli last to avoid circular imports
from .cli import main
__all__.append("main") 