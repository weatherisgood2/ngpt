try:
    from importlib.metadata import version as get_version
    __version__ = get_version("tOAI")
except ImportError:
    # For Python < 3.8 or package not installed
    __version__ = "0.2.0"  # fallback version

from .client import TOAIClient

__all__ = ["TOAIClient", "__version__"]

# Import cli last to avoid circular imports
from .cli import main
__all__.append("main") 