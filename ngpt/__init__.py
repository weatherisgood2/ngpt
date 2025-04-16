from importlib.metadata import version as get_version
__version__ = get_version("ngpt")

from .client import NGPTClient
from .config import load_config, get_config_path, get_config_dir

__all__ = ["NGPTClient", "__version__", "load_config", "get_config_path", "get_config_dir"]

# Import cli last to avoid circular imports
from .cli import main
__all__.append("main") 