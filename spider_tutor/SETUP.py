#!/usr/bin/env python3
"""
Spider Tutor - Interactive Setup Guide
Helps configure the application for your needs
"""

import os
from pathlib import Path

def show_banner():
    print("""
    ╔════════════════════════════════════════════════════════╗
    ║  🕷️  SPIDER TUTOR - Setup & Configuration Guide       ║
    ╚════════════════════════════════════════════════════════╝
    """)

def show_options():
    print("""
    ┌─ Choose Your Setup ─────────────────────────────────┐
    │                                                     │
    │  1️⃣  OpenAI (Recommended - Requires API Key)        │
    │      - Most reliable                               │
    │      - Faster responses                            │
    │      - Requires paid API key                       │
    │      Cost: ~$0.001-0.01 per question              │
    │                                                     │
    │  2️⃣  Ollama + Neural-Chat (Free - Local)           │
    │      - No API key needed                           │
    │      - Runs locally on your machine               │
    │      - Slower (depends on hardware)               │
    │      - Currently downloading...                    │
    │                                                     │
    │  3️⃣  Anthropic Claude (Requires API Key)           │
    │      - High quality responses                      │
    │      - Requires paid API key                       │
    │      Cost: ~$0.001-0.01 per question              │
    │                                                     │
    └─────────────────────────────────────────────────────┘
    """)

def setup_openai():
    print("\n" + "="*60)
    print("🔑 OpenAI Setup")
    print("="*60)
    print("""
    1. Get an API key:
       → Go to: https://platform.openai.com/account/api-keys
       → Create a new API key
       → Copy it to clipboard
    
    2. Add it to .env:
       Open: spider_tutor/.env
       Replace: OPENAI_API_KEY=sk-
       With:    OPENAI_API_KEY=sk-your-actual-key-here
    
    3. Test it:
       python main.py
       Ask: "What is the CIA triad?"
    
    💡 Tip: The gpt-4o-mini model is:
       - Fast and affordable
       - Perfect for cybersecurity education
       - Good quality responses
    """)

def setup_ollama():
    print("\n" + "="*60)
    print("🦙 Ollama (Neural-Chat) Setup")
    print("="*60)
    print("""
    Status: neural-chat model is being downloaded...
    Size: ~4.1GB (smaller and faster than llama3.2)
    
    Estimated time: 5-10 minutes
    
    Once ready:
    1. Edit .env file
    2. Change: LLM_PROVIDER=openai
       To:      LLM_PROVIDER=ollama
    3. Change: MODEL_NAME=gpt-4o-mini
       To:      MODEL_NAME=neural-chat
    4. Save and run: python main.py
    
    💡 Check progress with:
       ollama list
    
    Note: Requires Ollama server running:
       ollama serve  (in another terminal)
    """)

def setup_anthropic():
    print("\n" + "="*60)
    print("🤖 Anthropic Claude Setup")
    print("="*60)
    print("""
    1. Get an API key:
       → Go to: https://console.anthropic.com/account/keys
       → Create an API key
       → Copy it
    
    2. Edit .env file:
       ANTHROPIC_API_KEY=your-key-here
       LLM_PROVIDER=anthropic
       MODEL_NAME=claude-opus  (or claude-sonnet)
    
    3. Test it:
       python main.py
       Ask: "Explain the NIST Cybersecurity Framework"
    
    💡 Tip: Claude has strong reasoning abilities
       Perfect for complex cybersecurity scenarios
    """)

def show_current_config():
    print("\n" + "="*60)
    print("📋 Current Configuration")
    print("="*60)
    env_file = Path(__file__).parent / ".env"
    if env_file.exists():
        with open(env_file) as f:
            config = f.read()
            # Show only important lines
            for line in config.split('\n'):
                if line.startswith(('LLM_PROVIDER', 'MODEL_NAME', 'OPENAI_API_KEY', 'ANTHROPIC_API_KEY', 'OLLAMA')):
                    if 'KEY' in line and len(line.split('=')[1].strip()) > 2:
                        print(f"✅ {line.split('=')[0]} = ••••••••••••")
                    else:
                        print(f"   {line}")

if __name__ == "__main__":
    show_banner()
    show_options()
    show_current_config()
    
    print("\n" + "="*60)
    print("🚀 Quick Start")
    print("="*60)
    print("""
    Option A: Use OpenAI (Recommended)
    → Add your OpenAI API key to .env
    → Run: python main.py
    → Start asking questions!
    
    Option B: Wait for Ollama
    → Monitor with: ollama list
    → Once neural-chat is ready, edit .env
    → Change LLM_PROVIDER to 'ollama'
    → Run: python main.py
    
    Option C: Use Anthropic
    → Add your Anthropic API key to .env
    → Edit .env: LLM_PROVIDER=anthropic
    → Run: python main.py
    """)
    
    print("\n📚 Learn More:")
    print("   Cybersecurity Topics: https://www.nist.gov/")
    print("   MITRE ATT&CK: https://attack.mitre.org/")
    print("   CIS Controls: https://www.cisecurity.org/")
