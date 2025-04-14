import argparse
import sys
import os
from dotenv import load_dotenv
from .client import TOAIClient

# Load environment variables from .env file
load_dotenv()

def main():
    parser = argparse.ArgumentParser(description="tOAI - A CLI tool for interacting with custom OpenAI API endpoints")
    
    # Global options
    parser.add_argument('--api-key', default=os.getenv("OPENAI_API_KEY"), help='API key for the service')
    parser.add_argument('--base-url', default=os.getenv("OPENAI_BASE_URL"), help='Base URL for the API')
    parser.add_argument('--provider', default=os.getenv("OPENAI_PROVIDER"), help='Provider name')
    parser.add_argument('--model', default=os.getenv("OPENAI_MODEL"), help='Model to use')
    parser.add_argument('--web-search', action='store_true', 
                      help='Enable web search capability (Note: Your API endpoint must support this feature)')
    
    # Create subparsers for commands
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Chat command
    chat_parser = subparsers.add_parser('chat', help='Chat with the AI model')
    chat_parser.add_argument('prompt', nargs='?', default=None, help='The prompt to send')
    
    # Shell command
    shell_parser = subparsers.add_parser('shell', help='Generate and execute shell commands (Experimental)')
    shell_parser.add_argument('prompt', help='Description of the shell command to generate')
    
    # Code command
    code_parser = subparsers.add_parser('code', help='Generate code (Experimental)')
    code_parser.add_argument('prompt', help='Description of the code to generate')
    code_parser.add_argument('--language', default="python", help='Programming language to generate code in')
    
    args = parser.parse_args()
    
    # Initialize client
    client = TOAIClient(
        api_key=args.api_key,
        base_url=args.base_url,
        provider=args.provider,
        model=args.model
    )
    
    # Handle commands
    if args.command == 'chat':
        prompt = args.prompt
        if prompt is None:
            print("Enter your prompt: ", end='')
            prompt = input()
        client.chat(prompt, web_search=args.web_search)
        
    elif args.command == 'shell':
        command = client.generate_shell_command(args.prompt, web_search=args.web_search)
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
                
    elif args.command == 'code':
        generated_code = client.generate_code(args.prompt, args.language, web_search=args.web_search)
        print(f"\nGenerated code:\n{generated_code}")
        
    else:
        parser.print_help()
        
if __name__ == "__main__":
    main() 