"""
Spider Cybersecurity Tutor - AI Engine
Handles LLM integration for generating responses
"""

from typing import Optional, List, Dict, Generator
from dataclasses import dataclass, field
from rich.console import Console
import json

console = Console()

# Import LLM libraries
try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

try:
    import anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False

try:
    import ollama
    OLLAMA_AVAILABLE = True
except ImportError:
    OLLAMA_AVAILABLE = False


@dataclass
class Message:
    """Represents a chat message"""
    role: str  # 'user', 'assistant', 'system'
    content: str


@dataclass
class Conversation:
    """Manages conversation history"""
    messages: List[Message] = field(default_factory=list)
    max_history: int = 20
    
    def add_message(self, role: str, content: str):
        """Add a message to the conversation"""
        self.messages.append(Message(role=role, content=content))
        
        # Trim history if too long (keep system message)
        if len(self.messages) > self.max_history:
            system_msgs = [m for m in self.messages if m.role == 'system']
            other_msgs = [m for m in self.messages if m.role != 'system']
            self.messages = system_msgs + other_msgs[-(self.max_history - len(system_msgs)):]
    
    def get_messages_for_api(self) -> List[Dict]:
        """Convert messages to API format"""
        return [{"role": m.role, "content": m.content} for m in self.messages]
    
    def clear(self, keep_system: bool = True):
        """Clear conversation history"""
        if keep_system:
            self.messages = [m for m in self.messages if m.role == 'system']
        else:
            self.messages = []


class AIEngine:
    """Handles communication with LLM providers"""
    
    def __init__(self,
                 provider: str = "openai",
                 api_key: Optional[str] = None,
                 model: str = "gpt-4o-mini",
                 max_tokens: int = 2048,
                 temperature: float = 0.7,
                 system_prompt: str = ""):
        
        self.provider = provider.lower()
        self.model = model
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.system_prompt = system_prompt
        self.conversation = Conversation()
        self.client = None
        
        # Initialize the appropriate client
        self._init_client(api_key)
        
        # Add system prompt to conversation
        if system_prompt:
            self.conversation.add_message("system", system_prompt)
    
    def _init_client(self, api_key: Optional[str]):
        """Initialize the LLM client"""
        try:
            if self.provider == "openai" and OPENAI_AVAILABLE:
                if not api_key:
                    console.print("[red]❌ OpenAI API key required[/red]")
                    return
                self.client = openai.OpenAI(api_key=api_key)
                console.print(f"[green]🤖 OpenAI client initialized (model: {self.model})[/green]")
                
            elif self.provider == "anthropic" and ANTHROPIC_AVAILABLE:
                if not api_key:
                    console.print("[red]❌ Anthropic API key required[/red]")
                    return
                self.client = anthropic.Anthropic(api_key=api_key)
                self.model = "claude-3-haiku-20240307" if "haiku" in self.model.lower() else "claude-3-5-sonnet-20241022"
                console.print(f"[green]🤖 Anthropic client initialized (model: {self.model})[/green]")
                
            elif self.provider == "ollama" and OLLAMA_AVAILABLE:
                # Ollama runs locally, no API key needed
                self.client = ollama
                self.model = self.model or "llama3.2"
                console.print(f"[green]🤖 Ollama client initialized (model: {self.model})[/green]")
                
            else:
                console.print(f"[red]❌ Provider '{self.provider}' not available[/red]")
                
        except Exception as e:
            console.print(f"[red]❌ Failed to initialize AI client: {e}[/red]")
    
    def chat(self, user_message: str, stream: bool = False) -> str:
        """
        Send a message and get a response
        
        Args:
            user_message: User's input message
            stream: If True, stream the response
            
        Returns:
            Assistant's response
        """
        if not self.client:
            return "❌ AI engine not initialized. Please check your API key and provider settings."
        
        # Add user message to conversation
        self.conversation.add_message("user", user_message)
        
        try:
            if self.provider == "openai":
                response = self._chat_openai(stream)
            elif self.provider == "anthropic":
                response = self._chat_anthropic(stream)
            elif self.provider == "ollama":
                response = self._chat_ollama(stream)
            else:
                response = "❌ Unknown provider"
            
            # Add assistant response to conversation
            self.conversation.add_message("assistant", response)
            return response
            
        except Exception as e:
            error_msg = f"❌ Error generating response: {str(e)}"
            console.print(f"[red]{error_msg}[/red]")
            return error_msg
    
    def _chat_openai(self, stream: bool = False) -> str:
        """Chat using OpenAI API"""
        messages = self.conversation.get_messages_for_api()
        
        if stream:
            response_text = ""
            stream_response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                stream=True
            )
            for chunk in stream_response:
                if chunk.choices[0].delta.content:
                    content = chunk.choices[0].delta.content
                    response_text += content
                    print(content, end="", flush=True)
            print()  # Newline after streaming
            return response_text
        else:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=self.max_tokens,
                temperature=self.temperature
            )
            return response.choices[0].message.content
    
    def _chat_anthropic(self, stream: bool = False) -> str:
        """Chat using Anthropic API"""
        # Anthropic handles system prompt separately
        messages = [m for m in self.conversation.get_messages_for_api() if m['role'] != 'system']
        system = self.system_prompt
        
        if stream:
            response_text = ""
            with self.client.messages.stream(
                model=self.model,
                max_tokens=self.max_tokens,
                system=system,
                messages=messages
            ) as stream_response:
                for text in stream_response.text_stream:
                    response_text += text
                    print(text, end="", flush=True)
            print()
            return response_text
        else:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                system=system,
                messages=messages
            )
            return response.content[0].text
    
    def _chat_ollama(self, stream: bool = False) -> str:
        """Chat using Ollama (local)"""
        messages = self.conversation.get_messages_for_api()
        
        if stream:
            response_text = ""
            stream_response = self.client.chat(
                model=self.model,
                messages=messages,
                stream=True
            )
            for chunk in stream_response:
                content = chunk['message']['content']
                response_text += content
                print(content, end="", flush=True)
            print()
            return response_text
        else:
            response = self.client.chat(
                model=self.model,
                messages=messages
            )
            return response['message']['content']
    
    def reset_conversation(self):
        """Reset the conversation history"""
        self.conversation.clear(keep_system=True)
        console.print("[cyan]🔄 Conversation reset[/cyan]")
    
    def get_conversation_summary(self) -> str:
        """Get a summary of the current conversation"""
        msg_count = len([m for m in self.conversation.messages if m.role != 'system'])
        return f"Conversation: {msg_count} messages"