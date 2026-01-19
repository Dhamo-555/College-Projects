"""
Spider Cybersecurity Tutor - Voice Module
Handles Speech-to-Text (STT) and Text-to-Speech (TTS)
"""

import threading
import queue
from typing import Optional, Callable
from rich.console import Console

console = Console()

# Try importing voice libraries
try:
    import speech_recognition as sr
    STT_AVAILABLE = True
except ImportError:
    STT_AVAILABLE = False
    console.print("[yellow]⚠️ SpeechRecognition not installed. Voice input disabled.[/yellow]")

try:
    import pyttsx3
    PYTTSX3_AVAILABLE = True
except ImportError:
    PYTTSX3_AVAILABLE = False

try:
    from gtts import gTTS
    import playsound
    import tempfile
    import os
    GTTS_AVAILABLE = True
except ImportError:
    GTTS_AVAILABLE = False


class VoiceInput:
    """Handles speech-to-text conversion"""
    
    def __init__(self, engine: str = "google"):
        self.engine = engine
        self.recognizer = sr.Recognizer() if STT_AVAILABLE else None
        self.microphone = None
        self.is_listening = False
        
        if STT_AVAILABLE:
            try:
                self.microphone = sr.Microphone()
                # Adjust for ambient noise
                with self.microphone as source:
                    self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                console.print("[green]🎤 Microphone initialized[/green]")
            except Exception as e:
                console.print(f"[yellow]⚠️ Microphone error: {e}[/yellow]")
                self.microphone = None
    
    def listen(self, timeout: int = 5, phrase_limit: int = 15) -> Optional[str]:
        """
        Listen for voice input and convert to text
        
        Args:
            timeout: Seconds to wait for speech to start
            phrase_limit: Maximum seconds of speech to capture
            
        Returns:
            Transcribed text or None if failed
        """
        if not STT_AVAILABLE or not self.microphone:
            return None
        
        try:
            console.print("[cyan]🎤 Listening...[/cyan]")
            self.is_listening = True
            
            with self.microphone as source:
                audio = self.recognizer.listen(
                    source, 
                    timeout=timeout,
                    phrase_time_limit=phrase_limit
                )
            
            console.print("[cyan]🔄 Processing speech...[/cyan]")
            
            # Use Google Speech Recognition (free, no API key needed)
            if self.engine == "google":
                text = self.recognizer.recognize_google(audio)
            else:
                text = self.recognizer.recognize_google(audio)
            
            self.is_listening = False
            return text
            
        except sr.WaitTimeoutError:
            console.print("[yellow]⏱️ No speech detected[/yellow]")
            return None
        except sr.UnknownValueError:
            console.print("[yellow]❓ Could not understand audio[/yellow]")
            return None
        except sr.RequestError as e:
            console.print(f"[red]❌ Speech recognition error: {e}[/red]")
            return None
        finally:
            self.is_listening = False
    
    def listen_continuous(self, callback: Callable[[str], None], stop_phrase: str = "stop listening"):
        """
        Continuously listen and call callback with transcribed text
        
        Args:
            callback: Function to call with transcribed text
            stop_phrase: Phrase to stop listening
        """
        console.print(f"[cyan]🎤 Continuous listening started. Say '{stop_phrase}' to stop.[/cyan]")
        
        while True:
            text = self.listen()
            if text:
                if stop_phrase.lower() in text.lower():
                    console.print("[cyan]🛑 Stopping continuous listening[/cyan]")
                    break
                callback(text)


class VoiceOutput:
    """Handles text-to-speech conversion"""
    
    def __init__(self, engine: str = "pyttsx3", rate: int = 175):
        self.engine_name = engine
        self.rate = rate
        self.engine = None
        self.is_speaking = False
        self.speech_queue = queue.Queue()
        
        self._init_engine()
    
    def _init_engine(self):
        """Initialize the TTS engine"""
        if self.engine_name == "pyttsx3" and PYTTSX3_AVAILABLE:
            try:
                self.engine = pyttsx3.init()
                self.engine.setProperty('rate', self.rate)
                
                # Try to set a natural voice
                voices = self.engine.getProperty('voices')
                if voices:
                    # Prefer female voice if available (often clearer)
                    for voice in voices:
                        if 'female' in voice.name.lower() or 'zira' in voice.name.lower():
                            self.engine.setProperty('voice', voice.id)
                            break
                
                console.print("[green]🔊 TTS engine (pyttsx3) initialized[/green]")
            except Exception as e:
                console.print(f"[yellow]⚠️ pyttsx3 error: {e}[/yellow]")
                self.engine = None
                
        elif self.engine_name == "gtts" and GTTS_AVAILABLE:
            console.print("[green]🔊 TTS engine (gTTS) ready[/green]")
        else:
            console.print("[yellow]⚠️ No TTS engine available[/yellow]")
    
    def speak(self, text: str, block: bool = True):
        """
        Convert text to speech
        
        Args:
            text: Text to speak
            block: If True, wait for speech to complete
        """
        if not text:
            return
        
        # Clean text for speech
        clean_text = self._clean_for_speech(text)
        
        if self.engine_name == "pyttsx3" and self.engine:
            self._speak_pyttsx3(clean_text, block)
        elif self.engine_name == "gtts" and GTTS_AVAILABLE:
            self._speak_gtts(clean_text)
        else:
            # Fallback: just print
            console.print(f"[dim]🔇 (TTS disabled) {clean_text[:100]}...[/dim]")
    
    def _speak_pyttsx3(self, text: str, block: bool):
        """Speak using pyttsx3"""
        try:
            self.is_speaking = True
            self.engine.say(text)
            if block:
                self.engine.runAndWait()
            self.is_speaking = False
        except Exception as e:
            console.print(f"[red]❌ TTS error: {e}[/red]")
            self.is_speaking = False
    
    def _speak_gtts(self, text: str):
        """Speak using Google TTS"""
        try:
            self.is_speaking = True
            tts = gTTS(text=text, lang='en', slow=False)
            
            # Save to temp file and play
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as fp:
                temp_path = fp.name
                tts.save(temp_path)
            
            playsound.playsound(temp_path)
            os.unlink(temp_path)
            self.is_speaking = False
        except Exception as e:
            console.print(f"[red]❌ gTTS error: {e}[/red]")
            self.is_speaking = False
    
    def _clean_for_speech(self, text: str) -> str:
        """Clean text for better speech output"""
        import re
        
        # Remove markdown formatting
        text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)  # Bold
        text = re.sub(r'\*(.+?)\*', r'\1', text)      # Italic
        text = re.sub(r'`(.+?)`', r'\1', text)        # Code
        text = re.sub(r'#{1,6}\s*', '', text)         # Headers
        text = re.sub(r'\[(.+?)\]\(.+?\)', r'\1', text)  # Links
        
        # Remove emojis (keep text readable)
        text = re.sub(r'[🕷️🛡️📋✅❌⚠️🔒🔓💡📚🎯]', '', text)
        
        # Clean up extra whitespace
        text = re.sub(r'\n+', '. ', text)
        text = re.sub(r'\s+', ' ', text)
        
        return text.strip()
    
    def stop(self):
        """Stop current speech"""
        if self.engine_name == "pyttsx3" and self.engine:
            try:
                self.engine.stop()
            except:
                pass
        self.is_speaking = False


class VoiceManager:
    """Manages both voice input and output"""
    
    def __init__(self, 
                 voice_enabled: bool = True,
                 tts_engine: str = "pyttsx3",
                 stt_engine: str = "google",
                 voice_rate: int = 175):
        
        self.enabled = voice_enabled
        
        if voice_enabled:
            self.input = VoiceInput(engine=stt_engine)
            self.output = VoiceOutput(engine=tts_engine, rate=voice_rate)
        else:
            self.input = None
            self.output = None
            console.print("[yellow]🔇 Voice features disabled[/yellow]")
    
    def listen(self, timeout: int = 5) -> Optional[str]:
        """Listen for voice input"""
        if self.input:
            return self.input.listen(timeout=timeout)
        return None
    
    def speak(self, text: str, block: bool = True):
        """Speak text"""
        if self.output:
            self.output.speak(text, block=block)
    
    def is_available(self) -> bool:
        """Check if voice features are available"""
        return self.enabled and (self.input is not None or self.output is not None)