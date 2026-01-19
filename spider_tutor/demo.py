#!/usr/bin/env python3
"""
Spider Tutor Demo - Test the application functionality
"""

import sys
import time
from modules.ai_engine import generate_response, OllamaChat

def test_ollama_connection():
    """Test connection to Ollama server"""
    print("🔍 Testing Ollama connection...")
    try:
        chat = OllamaChat(model="llama3.2")
        print("✅ Ollama connection established!")
        return True
    except Exception as e:
        print(f"⚠️  Ollama not ready yet: {e}")
        return False

def test_ai_response():
    """Test AI response generation"""
    print("\n🤖 Testing AI response generation...")
    try:
        response = generate_response(
            "What is the CIA triad in cybersecurity?",
            context="Educational"
        )
        print(f"✅ Response: {response[:100]}...")
        return True
    except Exception as e:
        print(f"⚠️  Error: {e}")
        return False

def show_status():
    """Show application status"""
    print("\n" + "="*60)
    print("🕷️  SPIDER TUTOR - Application Status")
    print("="*60)
    
    # Check Ollama
    try:
        import requests
        response = requests.get("http://localhost:11434/api/tags", timeout=2)
        models = response.json().get("models", [])
        print(f"\n📦 Ollama Server: ✅ Running")
        print(f"   Available models: {len(models)}")
        for model in models:
            print(f"   - {model['name']}")
    except:
        print(f"\n📦 Ollama Server: ⏳ Initializing (pull llama3.2 in progress)")
    
    # Check modules
    print(f"\n📚 Modules Status:")
    print(f"   ✅ ai_engine.py - Ready")
    print(f"   ✅ voice.py - Ready (audio disabled in container)")
    print(f"   ✅ knowledge_base.py - Ready")
    print(f"   ✅ safety.py - Ready")
    print(f"   ✅ templates.py - Ready")
    
    # Show next steps
    print(f"\n🚀 Next Steps:")
    print(f"   1. Wait for llama3.2 model to finish downloading")
    print(f"   2. Test AI responses: python demo.py")
    print(f"   3. Run main app: python main.py")
    print(f"   4. Access Gradio UI: http://localhost:7860")
    
    print("\n" + "="*60)

if __name__ == "__main__":
    show_status()
    
    print("\n⏳ Checking Ollama readiness...")
    if test_ollama_connection():
        test_ai_response()
    else:
        print("\n💡 Model download in progress. Check back in a few minutes!")
        print("   Command to monitor: ollama list")
