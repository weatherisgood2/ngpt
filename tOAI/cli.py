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
    
    # Mode flags (mutually exclusive)
    mode_group = parser.add_mutually_exclusive_group()
    mode_group.add_argument('-s', '--shell', action='store_true', help='Generate and execute shell commands (Experimental)')
    mode_group.add_argument('-c', '--code', action='store_true', help='Generate code (Experimental)')
    
    # Language option for code mode
    parser.add_argument('--language', default="python", help='Programming language to generate code in (for code mode)')
    
    # Prompt argument
    parser.add_argument('prompt', nargs='?', default=None, help='The prompt to send')
    
    args = parser.parse_args()
    
    # Initialize client
    client = TOAIClient(
        api_key=args.api_key,
        base_url=args.base_url,
        provider=args.provider,
        model=args.model
    )
    
    # Handle modes
    if args.shell:
        if args.prompt is None:
            print("Enter shell command description: ", end='')
            prompt = input()
        else:
            prompt = args.prompt
            
        command = client.generate_shell_command(prompt, web_search=args.web_search)
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
        print(f"\nGenerated code:\n{generated_code}")
        
    else:
        # Default to chat mode
        if args.prompt is None:
            print("Enter your prompt: ", end='')
            prompt = input()
        else:
            prompt = args.prompt
        client.chat(prompt, web_search=args.web_search)
        
if __name__ == "__main__":
    main() 