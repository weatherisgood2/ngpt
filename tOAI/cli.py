import argparse
import sys
import os
from .client import TOAIClient
from .config import load_config, get_config_path
from . import __version__

def show_config_help():
    """Display help information about configuration."""
    print("\nConfiguration Help:")
    print("  1. Create a config file at one of these locations:")
    if sys.platform == "win32":
        print(f"     - %APPDATA%\\tOAI\\tOAI.conf")
    elif sys.platform == "darwin":
        print(f"     - ~/Library/Application Support/tOAI/tOAI.conf")
    else:
        print(f"     - ~/.config/tOAI/tOAI.conf")
    
    print("  2. Format your config file as JSON:")
    print("""     {
       "api_key": "your-api-key-here",
       "base_url": "https://api.openai.com/v1/",
       "provider": "OpenAI",
       "model": "gpt-3.5-turbo"
     }""")
    
    print("  3. Or set environment variables:")
    print("     - OPENAI_API_KEY")
    print("     - OPENAI_BASE_URL")
    print("     - OPENAI_PROVIDER")
    print("     - OPENAI_MODEL")
    
    print("  4. Or provide command line arguments:")
    print("     tOAI --api-key your-key --base-url https://api.example.com \"Your prompt\"")

def check_config(config):
    """Check config for common issues and provide guidance."""
    if not config.get("api_key"):
        print("Error: API key is not set.")
        show_config_help()
        return False
        
    # Check for common URL mistakes
    base_url = config.get("base_url", "")
    if base_url and not (base_url.startswith("http://") or base_url.startswith("https://")):
        print(f"Warning: Base URL '{base_url}' doesn't start with http:// or https://")
    
    return True

def main():
    parser = argparse.ArgumentParser(description="tOAI - A CLI tool for interacting with custom OpenAI API endpoints")
    
    # Version flag
    parser.add_argument('-v', '--version', action='version', version=f'tOAI {__version__}', help='Show version information and exit')
    
    # Config option
    parser.add_argument('--config', help='Path to a custom configuration file')
    
    # Global options
    parser.add_argument('--api-key', help='API key for the service')
    parser.add_argument('--base-url', help='Base URL for the API')
    parser.add_argument('--provider', help='Provider name')
    parser.add_argument('--model', help='Model to use')
    parser.add_argument('--web-search', action='store_true', 
                      help='Enable web search capability (Note: Your API endpoint must support this feature)')
    
    # Mode flags (mutually exclusive)
    mode_group = parser.add_mutually_exclusive_group()
    mode_group.add_argument('-s', '--shell', action='store_true', help='Generate and execute shell commands')
    mode_group.add_argument('-c', '--code', action='store_true', help='Generate code')
    mode_group.add_argument('--show-config', action='store_true', help='Show the current configuration and exit')
    
    # Language option for code mode
    parser.add_argument('--language', default="python", help='Programming language to generate code in (for code mode)')
    
    # Prompt argument
    parser.add_argument('prompt', nargs='?', default=None, help='The prompt to send')
    
    args = parser.parse_args()
    
    # Load configuration
    config = load_config(args.config)
    
    # Command-line arguments override config settings
    if args.api_key:
        config["api_key"] = args.api_key
    if args.base_url:
        config["base_url"] = args.base_url
    if args.provider:
        config["provider"] = args.provider
    if args.model:
        config["model"] = args.model
    
    # Show config if requested
    if args.show_config:
        config_path = get_config_path(args.config)
        print(f"Configuration file: {config_path}")
        print(f"API Key: {'[Set]' if config['api_key'] else '[Not Set]'}")
        print(f"Base URL: {config['base_url']}")
        print(f"Provider: {config['provider']}")
        print(f"Model: {config['model']}")
        return
    
    # Check if prompt is required but not provided
    if not args.prompt and not (args.shell or args.code):
        parser.print_help()
        return
        
    # Check configuration
    if not check_config(config):
        return
    
    # Initialize client
    client = TOAIClient(**config)
    
    try:
        # Handle modes
        if args.shell:
            if args.prompt is None:
                print("Enter shell command description: ", end='')
                prompt = input()
            else:
                prompt = args.prompt
                
            command = client.generate_shell_command(prompt, web_search=args.web_search)
            if not command:
                return  # Error already printed by client
                
            print(f"\nGenerated command: {command}")
            
            print("Do you want to execute this command? [y/N] ", end='')
            response = input().lower()
            if response == 'y' or response == 'yes':
                import subprocess
                try:
                    result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
                    print(f"\nOutput:\n{result.stdout}")
                except subprocess.CalledProcessError as e:
                    print(f"\nError:\n{e.stderr}")
                    
        elif args.code:
            if args.prompt is None:
                print("Enter code description: ", end='')
                prompt = input()
            else:
                prompt = args.prompt
                
            generated_code = client.generate_code(prompt, args.language, web_search=args.web_search)
            if generated_code:
                print(f"\nGenerated code:\n{generated_code}")
            
        else:
            # Default to chat mode
            if args.prompt is None:
                print("Enter your prompt: ", end='')
                prompt = input()
            else:
                prompt = args.prompt
            client.chat(prompt, web_search=args.web_search)
    
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
    except Exception as e:
        print(f"Error: {e}")
        
if __name__ == "__main__":
    main() 