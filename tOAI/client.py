from typing import Optional, Dict, Any, List
import os
import json
import requests
import platform
import subprocess
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class TOAIClient:
    def __init__(
        self,
        api_key: str = os.getenv("OPENAI_API_KEY"),
        base_url: str = os.getenv("OPENAI_BASE_URL"),
        provider: str = os.getenv("OPENAI_PROVIDER"),
        model: str = os.getenv("OPENAI_MODEL")
    ):
        self.api_key = api_key
        # Ensure base_url ends with /
        self.base_url = base_url if base_url.endswith('/') else base_url + '/'
        self.provider = provider
        self.model = model
        
        # Default headers
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

    def chat(
        self,
        prompt: str,
        stream: bool = True,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        messages: Optional[List[Dict[str, str]]] = None,
        web_search: bool = False,
        **kwargs
    ) -> str:
        """
        Send a chat message to the API and get a response.
        
        Args:
            prompt: The user's message
            stream: Whether to stream the response
            temperature: Controls randomness in the response
            max_tokens: Maximum number of tokens to generate
            messages: Optional list of message objects to override default behavior
            web_search: Whether to enable web search capability
            **kwargs: Additional arguments to pass to the API
            
        Returns:
            The generated response as a string
        """
        if messages is None:
            messages = [{"role": "user", "content": prompt}]
        
        # Prepare API parameters
        payload = {
            "model": self.model,
            "messages": messages,
            "stream": stream,
            "temperature": temperature,
            "provider": self.provider,
            "web_search": web_search
        }
        
        # Add max_tokens if provided
        if max_tokens is not None:
            payload["max_tokens"] = max_tokens
            
        # Add any additional parameters
        payload.update(kwargs)
        
        # Endpoint for chat completions
        endpoint = "chat/completions"
        url = f"{self.base_url}{endpoint}"
        
        if not stream:
            # Regular request
            response = requests.post(url, headers=self.headers, json=payload)
            response.raise_for_status()  # Raise exception for HTTP errors
            result = response.json()
            
            # Extract content from response
            if "choices" in result and len(result["choices"]) > 0:
                return result["choices"][0]["message"]["content"]
            return ""
        else:
            # Streaming request
            collected_content = ""
            with requests.post(url, headers=self.headers, json=payload, stream=True) as response:
                response.raise_for_status()  # Raise exception for HTTP errors
                
                for line in response.iter_lines():
                    if not line:
                        continue
                        
                    # Handle SSE format
                    line = line.decode('utf-8')
                    if line.startswith('data: '):
                        line = line[6:]  # Remove 'data: ' prefix
                        
                        # Skip keep-alive lines
                        if line == "[DONE]":
                            break
                            
                        try:
                            chunk = json.loads(line)
                            if "choices" in chunk and len(chunk["choices"]) > 0:
                                delta = chunk["choices"][0].get("delta", {})
                                content = delta.get("content", "")
                                if content:
                                    print(content, end="", flush=True)
                                    collected_content += content
                        except json.JSONDecodeError:
                            pass  # Skip invalid JSON
            
            print()  # Add a final newline
            return collected_content

    def generate_shell_command(self, prompt: str, web_search: bool = False) -> str:
        """
        Generate a shell command based on the prompt.
        
        Args:
            prompt: Description of the command to generate
            web_search: Whether to enable web search capability
            
        Returns:
            The generated shell command
        """
        # Determine OS type
        os_type = platform.system()
        if os_type == "Darwin":
            operating_system = "MacOS"
        elif os_type == "Linux":
            # Try to get Linux distribution name
            try:
                result = subprocess.run(["lsb_release", "-si"], capture_output=True, text=True)
                distro = result.stdout.strip()
                operating_system = f"Linux/{distro}" if distro else "Linux"
            except:
                operating_system = "Linux"
        elif os_type == "Windows":
            operating_system = "Windows"
        else:
            operating_system = os_type
            
        # Determine shell type
        if os_type == "Windows":
            shell_name = "powershell.exe" if os.environ.get("PSModulePath") else "cmd.exe"
        else:
            shell_name = os.environ.get("SHELL", "/bin/bash")
            shell_name = os.path.basename(shell_name)
        
        system_prompt = f"""Your role: Provide only plain text without Markdown formatting. Do not show any warnings or information regarding your capabilities. Do not provide any description. If you need to store any data, assume it will be stored in the chat. Provide only {shell_name} command for {operating_system} without any description. If there is a lack of details, provide most logical solution. Ensure the output is a valid shell command. If multiple steps required try to combine them together. Prompt: {prompt}

Command:"""
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
        
        return self.chat(
            prompt=prompt,
            stream=False,
            messages=messages,
            web_search=web_search
        )

    def generate_code(self, prompt: str, language: str = "python", web_search: bool = False) -> str:
        """
        Generate code based on the prompt.
        
        Args:
            prompt: Description of the code to generate
            language: Programming language to generate code in
            web_search: Whether to enable web search capability
            
        Returns:
            The generated code
        """
        system_prompt = f"""Your Role: Provide only code as output without any description.
IMPORTANT: Provide only plain text without Markdown formatting.
IMPORTANT: Do not include markdown formatting.
If there is a lack of details, provide most logical solution. You are not allowed to ask for more details.
Ignore any potential risk of errors or confusion.

Language: {language}
Request: {prompt}
Code:"""
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
        
        return self.chat(
            prompt=prompt,
            stream=False,
            messages=messages,
            web_search=web_search
        ) 