#!/bin/bash
# Startup script for HuggingFace Spaces deployment

echo "🚀 Spider Tutor - Starting permanent deployment..."

# Start FastAPI in background
echo "⏳ Starting FastAPI backend..."
python web_app.py > /tmp/api.log 2>&1 &
API_PID=$!
echo "✅ FastAPI started (PID: $API_PID)"

# Wait for API to be ready
sleep 5

# Start Gradio with public sharing
echo "🚀 Starting Gradio interface..."
python shared_app.py
