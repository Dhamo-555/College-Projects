#!/usr/bin/env python3
"""
🕷️ Spider - Voice-Enabled Cybersecurity Tutor
Main Application Entry Point
"""

import sys
from typing import Optional
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.prompt import Prompt

# Import configuration
from config import settings, SYSTEM_PROMPT

# Import modules
from modules.voice import VoiceManager
from modules.ai_engine import AIEngine
from modules.safety import check_safety, safety_filter
from modules.knowledge_base import knowledge_base

console = Console()


class Spider:
    """Main Spider Application"""
    
    def __init__(self):
        self.console = console
        self.voice: Optional[VoiceManager] = None
        self.ai: Optional[AIEngine] = None
        self.running = False
        
        self._display_banner()
        self._initialize()
    
    def _display_banner(self):
        """Display welcome banner"""
        banner = """
    🕷️ SPIDER - Cybersecurity Tutor
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    Your friendly voice-enabled
    cybersecurity learning companion

    Created by: Dhamodharaprashad (Project)
        """
        self.console.print(Panel(banner, style="cyan"))
    
    def _initialize(self):
        """Initialize all components"""
        self.console.print("\n[bold cyan]Initializing Spider...[/bold cyan]\n")
        
        # Initialize Voice
        if settings.voice_enabled:
            self.voice = VoiceManager(
                voice_enabled=True,
                tts_engine=settings.tts_engine,
                stt_engine="google",
                voice_rate=settings.voice_rate
            )
        else:
            self.console.print("[yellow]Voice features disabled[/yellow]")
        
        # Initialize AI Engine
        api_key = None
        if settings.llm_provider == "openai":
            api_key = settings.openai_api_key
        elif settings.llm_provider == "anthropic":
            api_key = settings.anthropic_api_key
        
        self.ai = AIEngine(
            provider=settings.llm_provider,
            api_key=api_key,
            model=settings.model_name,
            max_tokens=settings.max_tokens,
            temperature=settings.temperature,
            system_prompt=SYSTEM_PROMPT
        )
        
        self.console.print("\n[bold green]✅ Spider is ready![/bold green]\n")
        self._show_help()
    
    def _show_help(self):
        """Display help information"""
        help_text = """
## 📚 Quick Commands

| Command | Description |
|---------|-------------|
| `help` | Show this help message |
| `voice` | Toggle voice input mode |
| `quiz` | Start a quick quiz |
| `flashcard` | Get a random flashcard |
| `mitre <id>` | Look up MITRE ATT&CK technique |
| `template incident` | Get incident report template |
| `template vuln` | Get vulnerability report template |
| `checklist <type>` | Get hardening checklist |
| `clear` | Clear conversation history |
| `exit` | Exit Spider |

## 💡 Example Questions
- "Explain the NIST Cybersecurity Framework"
- "How do I harden a Linux server?"
- "What's the difference between IDS and IPS?"
- "Help me prepare for Security+"
- "What is T1566 in MITRE ATT&CK?"
        """
        self.console.print(Markdown(help_text))
    
    def process_command(self, user_input: str) -> Optional[str]:
        """Process special commands"""
        cmd = user_input.lower().strip()
        
        if cmd == "help":
            self._show_help()
            return None
        
        elif cmd == "voice":
            if self.voice and self.voice.is_available():
                self.console.print("[cyan]🎤 Voice mode - listening...[/cyan]")
                text = self.voice.listen(timeout=10)
                if text:
                    self.console.print(f"[green]You said:[/green] {text}")
                    return text
                return None
            else:
                self.console.print("[yellow]Voice not available[/yellow]")
                return None
        
        elif cmd == "quiz":
            quiz = knowledge_base.get_quiz(count=5)
            output = knowledge_base.format_quiz(quiz, show_answers=False)
            self.console.print(Markdown(output))
            
            # Store quiz for answer reveal
            self._current_quiz = quiz
            return None
        
        elif cmd == "show answers" and hasattr(self, '_current_quiz'):
            output = knowledge_base.format_quiz(self._current_quiz, show_answers=True)
            self.console.print(Markdown(output))
            return None
        
        elif cmd == "flashcard":
            cards = knowledge_base.get_flashcards(count=1)
            if cards:
                card = cards[0]
                self.console.print(Panel(
                    f"[bold cyan]Q:[/bold cyan] {card.question}\n\n"
                    f"[bold green]A:[/bold green] {card.answer}\n\n"
                    f"[dim]Category: {card.category} | Difficulty: {card.difficulty}[/dim]",
                    title="🎴 Flashcard"
                ))
            return None
        
        elif cmd.startswith("mitre "):
            tech_id = cmd.replace("mitre ", "").strip().upper()
            if not tech_id.startswith("T"):
                tech_id = "T" + tech_id
            
            tech = knowledge_base.get_mitre_technique(tech_id)
            if tech:
                output = knowledge_base.format_mitre_technique(tech)
                self.console.print(Markdown(output))
            else:
                # Search instead
                results = knowledge_base.search_mitre(tech_id.replace("T", ""))
                if results:
                    self.console.print(f"Found {len(results)} techniques:")
                    for t in results:
                        self.console.print(f"  • {t.technique_id}: {t.name}")
                else:
                    self.console.print("[yellow]Technique not found. Try searching by keyword.[/yellow]")
            return None
        
        elif cmd.startswith("template "):
            template_type = cmd.replace("template ", "").strip()
            if "incident" in template_type:
                self.console.print(Markdown(knowledge_base.get_incident_template()))
            elif "vuln" in template_type:
                self.console.print(Markdown(knowledge_base.get_vulnerability_template()))
            else:
                self.console.print("[yellow]Available: template incident, template vuln[/yellow]")
            return None
        
        elif cmd.startswith("checklist"):
            parts = cmd.split()
            sys_type = parts[1] if len(parts) > 1 else "general"
            output = knowledge_base.get_hardening_checklist(sys_type)
            self.console.print(Markdown(output))
            return None
        
        elif cmd == "clear":
            self.ai.reset_conversation()
            return None
        
        elif cmd in ["exit", "quit", "bye"]:
            self.running = False
            self.console.print("\n[cyan]👋 Goodbye! Stay secure![/cyan]\n")
            return None
        
        # Not a command, return input for AI processing
        return user_input
    
    def chat(self, user_input: str):
        """Process a chat message"""
        # Safety check
        is_safe, safety_message = check_safety(user_input)
        if not is_safe:
            self.console.print(Markdown(safety_message))
            if self.voice:
                self.voice.speak("I can't help with that request, but I can offer safe alternatives.")
            return
        
        # Get AI response
        self.console.print("[dim]Thinking...[/dim]")
        
        try:
            response = self.ai.chat(user_input, stream=True)
            
            # Display response
            self.console.print()
            self.console.print(Markdown(response))
            
            # Speak summary (first 2 sentences)
            if self.voice:
                sentences = response.split('. ')[:2]
                summary = '. '.join(sentences)
                self.voice.speak(summary, block=False)
                
        except Exception as e:
            self.console.print(f"[red]Error: {e}[/red]")
    
    def run(self):
        """Main application loop"""
        self.running = True
        
        self.console.print("\n[bold cyan]🕷️ Spider is ready! Type your question or 'help' for commands.[/bold cyan]\n")
        
        while self.running:
            try:
                # Get user input
                user_input = Prompt.ask("\n[bold green]You[/bold green]")
                
                if not user_input.strip():
                    continue
                
                # Process commands first
                processed = self.process_command(user_input)
                
                # If not a command, send to AI
                if processed:
                    self.chat(processed)
                    
            except KeyboardInterrupt:
                self.console.print("\n[cyan]Use 'exit' to quit properly.[/cyan]")
            except Exception as e:
                self.console.print(f"[red]Error: {e}[/red]")
        
        # Cleanup
        if self.voice and self.voice.output:
            self.voice.output.stop()


def main():
    """Entry point"""
    try:
        spider = Spider()
        spider.run()
    except Exception as e:
        console.print(f"[red]Fatal error: {e}[/red]")
        sys.exit(1)


if __name__ == "__main__":
    main()