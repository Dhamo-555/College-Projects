#!/usr/bin/env python3
"""
Quick Start Guide - Choose Your Configuration
"""

def show_options():
    print("""
    ╔════════════════════════════════════════════════════════════╗
    ║  🕷️  SPIDER TUTOR - Memory Issue Resolution               ║
    ╚════════════════════════════════════════════════════════════╝
    
    ⚠️  Current Issue:
        System has 3.3 GB RAM available
        neural-chat needs 4.3 GB
        Downloading phi (2.7 GB) - smaller model
    
    💡 RECOMMENDED: Switch to OpenAI (No Memory Limit!)
    
    ┌─────────────────────────────────────────────────────────┐
    │ Option A: Use OpenAI (Immediate, Recommended)           │
    │                                                          │
    │ Steps:                                                   │
    │ 1. Get free API key from:                              │
    │    https://platform.openai.com/account/api-keys        │
    │                                                          │
    │ 2. Edit .env and add your key:                         │
    │    OPENAI_API_KEY=sk-your-key-here                     │
    │    LLM_PROVIDER=openai                                 │
    │    MODEL_NAME=gpt-4o-mini                              │
    │                                                          │
    │ 3. Run immediately:                                     │
    │    python main.py                                       │
    │                                                          │
    │ Cost: ~$0.001 per question (very affordable)           │
    │ Speed: Instant                                          │
    │ Quality: Excellent                                      │
    └─────────────────────────────────────────────────────────┘
    
    ┌─────────────────────────────────────────────────────────┐
    │ Option B: Wait for Phi Model (Free, ~10-15 min)        │
    │                                                          │
    │ Steps:                                                   │
    │ 1. Wait for phi to download (34% done)                 │
    │ 2. Automatically configured in .env                    │
    │ 3. Run when ready:                                      │
    │    python main.py                                       │
    │                                                          │
    │ Cost: Free                                              │
    │ Speed: Slow (depends on hardware)                       │
    │ Quality: Good for basic Q&A                            │
    │ Memory: Uses only 2.7 GB                               │
    └─────────────────────────────────────────────────────────┘
    
    ┌─────────────────────────────────────────────────────────┐
    │ Option C: Use Anthropic Claude (Requires API Key)      │
    │                                                          │
    │ Steps:                                                   │
    │ 1. Get API key from:                                   │
    │    https://console.anthropic.com/account/keys          │
    │                                                          │
    │ 2. Edit .env:                                          │
    │    ANTHROPIC_API_KEY=sk-ant-your-key                   │
    │    LLM_PROVIDER=anthropic                              │
    │    MODEL_NAME=claude-opus                              │
    │                                                          │
    │ 3. Run:                                                 │
    │    python main.py                                       │
    │                                                          │
    │ Cost: ~$0.001-0.01 per question                        │
    │ Speed: Very fast                                        │
    │ Quality: Excellent for reasoning                        │
    └─────────────────────────────────────────────────────────┘
    
    """)
    
    print("\n📊 Quick Comparison:\n")
    print("Provider        | Memory | Speed  | Cost   | Quality | Setup Time")
    print("─" * 65)
    print("OpenAI          | ✅ None| ⚡⚡⚡ | $$    | 🌟🌟🌟  | 5 min")
    print("Anthropic       | ✅ None| ⚡⚡⚡ | $$    | 🌟🌟🌟  | 5 min")
    print("Phi (Ollama)    | 2.7GB | 🐢    | Free  | 🌟🌟    | 15 min")
    print("\n")

if __name__ == "__main__":
    show_options()
    
    print("🎯 NEXT STEP:")
    print("\n1. Choose your preferred option above")
    print("2. For OpenAI: Get free API key (many free credits)")
    print("3. Add key to .env file")
    print("4. Run: python main.py")
    print("\n" + "="*65)
    print("\n📖 To see the full setup guide, run: python SETUP.py\n")
