#!/usr/bin/env python3
"""
Public tunnel setup for Spider Tutor
Uses pyngrok to expose local FastAPI app to the internet
"""

import subprocess
import time
import sys
from pyngrok import ngrok

def start_public_tunnel():
    """Start ngrok tunnel to expose the web app"""
    try:
        # Connect ngrok
        print("🌐 Starting public tunnel...")
        public_url = ngrok.connect(8000, "http")
        
        print("\n" + "="*60)
        print("✅ PUBLIC LINK IS READY!")
        print("="*60)
        print(f"\n🔗 Access your app here:\n   {public_url}\n")
        print("="*60)
        print("\nThis link is accessible from any device in the world!")
        print("The tunnel will stay active as long as this process runs.\n")
        
        # Keep the tunnel alive
        ngrok_process = ngrok.get_ngrok_process()
        ngrok_process.proc.wait()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    start_public_tunnel()
