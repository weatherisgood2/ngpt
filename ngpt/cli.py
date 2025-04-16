import argparse
import sys
import os
from .client import NGPTClient
from .config import load_config, get_config_path, load_configs, add_config_entry
from . import __version__

def show_config_help():
    """Display help information about configuration."""
    print("\nConfiguration Help:")
    print("  1. Create a config file at one of these locations:")
    if sys.platform == "win32":
        print(f"     - %APPDATA%\\ngpt\\ngpt.conf")
    elif sys.platform == "darwin":
        print(f"     - ~/Library/Application Support/ngpt/ngpt.conf")
    else:
        print(f"     - ~/.config/ngpt/ngpt.conf")
    
    print("  2. Format your config file as JSON:")
    print("""     [
       {
         "api_key": "your-api-key-here",
         "base_url": "https://api.openai.com/v1/",
         "provider": "OpenAI",
         "model": "gpt-3.5-turbo"
       },
       {
         "api_key": "your-second-api-key",
         "base_url": "http://localhost:1337/v1/",
         "provider": "Another Provider",
         "model": "different-model"
       }
     ]""")
    
    print("  3. Or set environment variables:")
    print("     - OPENAI_API_KEY")
    print("     - OPENAI_BASE_URL")
    print("     - OPENAI_MODEL")
    
    print("  4. Or provide command line arguments:")
    print("     ngpt --api-key your-key --base-url https://api.example.com --model your-model \"Your prompt\"")
    
    print("  5. Use --config-index to specify which configuration to use:")
    print("     ngpt --config-index 1 \"Your prompt\"")
    
    print("  6. Use --config without arguments to add or edit a configuration:")
    print("     ngpt --config --config-index 1")

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
    parser = argparse.ArgumentParser(description="nGPT - A CLI tool for interacting with custom OpenAI API endpoints")
    
    # Version flag
    parser.add_argument('-v', '--version', action='version', version=f'nGPT {__version__}', help='Show version information and exit')
    
    # Config options
    config_group = parser.add_argument_group('Configuration Options')
    config_group.add_argument('--config', nargs='?', const=True, help='Path to a custom config file or, if no value provided, enter interactive configuration mode')
    config_group.add_argument('--config-index', type=int, default=0, help='Index of the configuration to use (default: 0)')
    config_group.add_argument('--show-config', action='store_true', help='Show the current configuration(s) and exit')
    config_group.add_argument('--all', action='store_true', help='Show details for all configurations (requires --show-config)')
    
    # Global options
    global_group = parser.add_argument_group('Global Options')
    global_group.add_argument('--api-key', help='API key for the service')
    global_group.add_argument('--base-url', help='Base URL for the API')
    global_group.add_argument('--model', help='Model to use')
    global_group.add_argument('--web-search', action='store_true', 
                      help='Enable web search capability (Note: Your API endpoint must support this feature)')
    
    # Mode flags (mutually exclusive)
    mode_group = parser.add_argument_group('Modes (mutually exclusive)')
    mode_exclusive_group = mode_group.add_mutually_exclusive_group()
    mode_exclusive_group.add_argument('-s', '--shell', action='store_true', help='Generate and execute shell commands')
    mode_exclusive_group.add_argument('-c', '--code', action='store_true', help='Generate code')
    # Note: --show-config is handled separately and implicitly acts as a mode
    
    # Language option for code mode
    parser.add_argument('--language', default="python", help='Programming language to generate code in (for code mode)')
    
    # Prompt argument
    parser.add_argument('prompt', nargs='?', default=None, help='The prompt to send')
    
    args = parser.parse_args()
    
    # Validate --all usage
    if args.all and not args.show_config:
        parser.error("--all can only be used with --show-config")

    # Handle interactive configuration mode
    if args.config is True:  # --config was used without a value
        config_path = get_config_path()
        add_config_entry(config_path, args.config_index)
        return
    
    # Load configuration using the specified index (needed for active config display)
    active_config = load_config(args.config, args.config_index)
    
    # Command-line arguments override config settings for active config display
    # This part is kept to ensure the active config display reflects potential overrides,
    # even though the overrides don't affect the stored configurations displayed with --all.
    if args.api_key:
        active_config["api_key"] = args.api_key
    if args.base_url:
        active_config["base_url"] = args.base_url
    if args.model:
        active_config["model"] = args.model
    
    # Show config if requested
    if args.show_config:
        config_path = get_config_path(args.config)
        configs = load_configs(args.config)
        
        print(f"Configuration file: {config_path}")
        print(f"Total configurations: {len(configs)}")
        print(f"Active configuration index: {args.config_index}")

        if args.all:
            # Show details for all configurations
            print("\nAll configuration details:")
            for i, cfg in enumerate(configs):
                active_str = '(Active)' if i == args.config_index else ''
                print(f"\n--- Configuration Index {i} {active_str} ---")
                print(f"  API Key: {'[Set]' if cfg.get('api_key') else '[Not Set]'}")
                print(f"  Base URL: {cfg.get('base_url', 'N/A')}")
                print(f"  Provider: {cfg.get('provider', 'N/A')}")
                print(f"  Model: {cfg.get('model', 'N/A')}")
        else:
            # Show active config details and summary list
            print("\nActive configuration details:")
            print(f"  API Key: {'[Set]' if active_config.get('api_key') else '[Not Set]'}")
            print(f"  Base URL: {active_config.get('base_url', 'N/A')}")
            print(f"  Provider: {active_config.get('provider', 'N/A')}")
            print(f"  Model: {active_config.get('model', 'N/A')}")
            
            if len(configs) > 1:
                print("\nAvailable configurations:")
                for i, cfg in enumerate(configs):
                    active_marker = "*" if i == args.config_index else " "
                    print(f"[{i}]{active_marker} {cfg.get('provider', 'N/A')} - {cfg.get('model', 'N/A')} ({'[API Key Set]' if cfg.get('api_key') else '[API Key Not Set]'})")
        
        return
    
    # Check if prompt is required but not provided
    if not args.prompt and not (args.shell or args.code):
        parser.print_help()
        return
        
    # Check configuration (using the potentially overridden active_config)
    if not check_config(active_config):
        return
    
    # Initialize client using the potentially overridden active_config
    client = NGPTClient(**active_config)
    
    try:
        # Handle modes
        if args.shell:
            if args.prompt is None:
                try:
                    print("Enter shell command description: ", end='')
                    prompt = input()
                except KeyboardInterrupt:
                    print("\nInput cancelled by user. Exiting gracefully.")
                    sys.exit(130)
            else:
                prompt = args.prompt
                
            command = client.generate_shell_command(prompt, web_search=args.web_search)
            if not command:
                return  # Error already printed by client
                
            print(f"\nGenerated command: {command}")
            
            try:
                print("Do you want to execute this command? [y/N] ", end='')
                response = input().lower()
            except KeyboardInterrupt:
                print("\nCommand execution cancelled by user.")
                return
                
            if response == 'y' or response == 'yes':
                import subprocess
                try:
                    try:
                        print("\nExecuting command... (Press Ctrl+C to cancel)")
                        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
                        print(f"\nOutput:\n{result.stdout}")
                    except KeyboardInterrupt:
                        print("\nCommand execution cancelled by user.")
                except subprocess.CalledProcessError as e:
                    print(f"\nError:\n{e.stderr}")
                    
        elif args.code:
            if args.prompt is None:
                try:
                    print("Enter code description: ", end='')
                    prompt = input()
                except KeyboardInterrupt:
                    print("\nInput cancelled by user. Exiting gracefully.")
                    sys.exit(130)
            else:
                prompt = args.prompt
                
            generated_code = client.generate_code(prompt, args.language, web_search=args.web_search)
            if generated_code:
                print(f"\nGenerated code:\n{generated_code}")
            
        else:
            # Default to chat mode
            if args.prompt is None:
                try:
                    print("Enter your prompt: ", end='')
                    prompt = input()
                except KeyboardInterrupt:
                    print("\nInput cancelled by user. Exiting gracefully.")
                    sys.exit(130)
            else:
                prompt = args.prompt
            client.chat(prompt, web_search=args.web_search)
    
    except KeyboardInterrupt:
        print("\nOperation cancelled by user. Exiting gracefully.")
        # Make sure we exit with a non-zero status code to indicate the operation was cancelled
        sys.exit(130)  # 130 is the standard exit code for SIGINT (Ctrl+C)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)  # Exit with error code

if __name__ == "__main__":
    main() 