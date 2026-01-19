#!/usr/bin/env python3
"""
Monitor Ollama model download progress and auto-run Spider once ready
"""

import time
import subprocess
import sys
from pathlib import Path

def check_model_ready():
    """Check if neural-chat model is ready"""
    try:
        result = subprocess.run(['ollama', 'list'], capture_output=True, text=True, timeout=5)
        models = result.stdout
        return 'neural-chat' in models
    except:
        return False

def wait_for_model():
    """Wait for neural-chat to be ready"""
    print("⏳ Waiting for neural-chat model to download...\n")
    
    start_time = time.time()
    while not check_model_ready():
        elapsed = int(time.time() - start_time)
        dots = "." * (elapsed % 4)
        print(f"\r⏳ Still downloading {dots:<3}", end="", flush=True)
        time.sleep(1)
    
    print("\n\n✅ Neural-chat model is ready!\n")
    return True

def run_spider():
    """Run the Spider application"""
    print("🕷️  Starting Spider Tutor...\n")
    spider_dir = Path(__file__).parent
    
    try:
        subprocess.run(
            ['python', 'main.py'],
            cwd=spider_dir,
            check=False
        )
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
        sys.exit(0)

if __name__ == "__main__":
    if check_model_ready():
        print("✅ Neural-chat is already ready!\n")
    else:
        wait_for_model()
    
    # Verify config is set correctly
    print("📋 Verifying configuration...")
    env_file = Path(__file__).parent / ".env"
    
    with open(env_file) as f:
        env_content = f.read()
    
    if 'LLM_PROVIDER=ollama' in env_content and 'MODEL_NAME=neural-chat' in env_content:
        print("✅ Configuration is correct\n")
        run_spider()
    else:
        print("⚠️  Configuration needs update!")
        print("\nPlease ensure .env has:")
        print("  LLM_PROVIDER=ollama")
        print("  MODEL_NAME=neural-chat")
        print("\nThen run: python main.py")
