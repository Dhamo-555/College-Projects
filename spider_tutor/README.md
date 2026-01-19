# 🕷️ Spider Tutor - AI-Powered Cybersecurity Tutor

A voice-enabled, AI-powered cybersecurity tutoring system with knowledge base integration, safety filtering, and flexible LLM provider support.

## ⚡ Quick Start

### Prerequisites
- Python 3.10+
- Virtual environment (included)
- Internet connection (for API-based LLMs)

### Installation

```bash
# Navigate to project directory
cd spider_tutor

# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies (if not already done)
pip install -r requirements.txt

# Configure your LLM provider (see below)
# Then run the application
python main.py
```

## 🤖 LLM Provider Setup

Choose one of three options:

### Option 1: OpenAI (Recommended) ⭐

**Best for:** Reliability, speed, and quality

```bash
# 1. Get API key from https://platform.openai.com/account/api-keys
# 2. Edit .env file and add:
OPENAI_API_KEY=sk-your-api-key-here
LLM_PROVIDER=openai
MODEL_NAME=gpt-4o-mini

# 3. Run
python main.py
```

**Cost:** ~$0.001-0.01 per question  
**Model:** gpt-4o-mini (fast, affordable, perfect for education)

### Option 2: Ollama + Neural-Chat (Free, Local) 🦙

**Best for:** Privacy, no API costs, offline capability

```bash
# 1. Install Ollama (if not done)
curl -fsSL https://ollama.ai/install.sh | sh

# 2. Start Ollama server in another terminal
ollama serve

# 3. Pull neural-chat model
ollama pull neural-chat

# 4. Edit .env file:
LLM_PROVIDER=ollama
MODEL_NAME=neural-chat
OLLAMA_HOST=http://localhost:11434

# 5. Run Spider
python main.py
```

**Cost:** Free  
**Model Size:** ~4.1GB  
**Speed:** Depends on your hardware

### Option 3: Anthropic Claude (High Quality) 🤖

**Best for:** Complex reasoning, detailed explanations

```bash
# 1. Get API key from https://console.anthropic.com/account/keys
# 2. Edit .env file:
ANTHROPIC_API_KEY=sk-ant-your-key-here
LLM_PROVIDER=anthropic
MODEL_NAME=claude-opus

# 3. Run
python main.py
```

**Cost:** ~$0.001-0.01 per question  
**Model:** Claude Opus (excellent for cybersecurity scenarios)

## 📖 Usage

### Interactive Commands

```
🕷️ Spider is ready! Type your question or 'help' for commands.

Commands:
  help                  Show help message
  quiz                  Start a cybersecurity quiz
  flashcard             Get a random study flashcard
  mitre T1234           Look up MITRE ATT&CK technique
  template incident     Get incident report template
  template vuln         Get vulnerability report template
  checklist hardening   Get security hardening checklist
  clear                 Clear conversation history
  exit                  Exit Spider
```

### Example Questions

```
"Explain the CIA triad in cybersecurity"
"What is a zero-day vulnerability?"
"How do I harden a Linux server?"
"What's the difference between IDS and IPS?"
"Help me prepare for Security+ exam"
"What is T1566 in MITRE ATT&CK?"
"Explain the NIST Cybersecurity Framework"
"What are the CIS Top 18 Controls?"
```

## 📁 Project Structure

```
spider_tutor/
├── main.py                 # Main application entry point
├── config.py               # Configuration & settings
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (API keys)
├── SETUP.py               # Interactive setup guide
├── demo.py                # Demo & testing script
│
├── modules/
│   ├── __init__.py
│   ├── voice.py            # Speech-to-text & text-to-speech
│   ├── ai_engine.py        # LLM integration (OpenAI, Anthropic, Ollama)
│   ├── knowledge_base.py   # Cybersecurity knowledge base
│   ├── safety.py           # Content filtering & safety
│   └── templates.py        # Report templates & utilities
│
├── data/
│   ├── flashcards.json     # Study flashcards
│   └── mitre_mapping.json  # MITRE ATT&CK framework data
│
└── README.md              # This file
```

## 🔧 Configuration

### Environment Variables (.env)

```bash
# LLM Provider Configuration
LLM_PROVIDER=openai              # Choose: openai, anthropic, ollama
MODEL_NAME=gpt-4o-mini          # Model to use for that provider
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=neural-chat         # Alternative: llama3.2, mistral

# API Keys (required for cloud providers)
OPENAI_API_KEY=                  # Leave blank if using Ollama
ANTHROPIC_API_KEY=               # Leave blank if using other providers
ELEVENLABS_API_KEY=              # For advanced voice features (optional)

# Application Settings
DEBUG=False
LOG_LEVEL=INFO
VOICE_ENABLED=false              # Voice features require PyAudio
MAX_TOKENS=2048
TEMPERATURE=0.7
```

## 🚀 Features

✅ **Multi-LLM Support**
  - OpenAI (gpt-4, gpt-4o-mini, gpt-3.5-turbo)
  - Anthropic Claude (Opus, Sonnet, Haiku)
  - Ollama local models (llama3.2, neural-chat, mistral)

✅ **Cybersecurity Focus**
  - NIST Cybersecurity Framework guidance
  - MITRE ATT&CK technique lookups
  - CIS Controls mapping
  - Security+ exam preparation
  - Incident response templates

✅ **Safety Features**
  - Content filtering
  - Ensures legal, ethical guidance
  - Blocks harmful request patterns
  - Educational focus only

✅ **Learning Tools**
  - Interactive flashcards
  - Quizzes & assessments
  - Report templates
  - Hardening checklists

✅ **Voice Support** (when audio available)
  - Speech-to-text input
  - Text-to-speech output
  - Multiple TTS engines

## 📊 Comparison: LLM Providers

| Feature | OpenAI | Anthropic | Ollama |
|---------|--------|-----------|--------|
| Cost | $$ | $$ | Free |
| Speed | Very Fast | Fast | Slow |
| Quality | Excellent | Excellent | Good |
| Internet | Required | Required | Optional |
| Setup | Easy | Easy | Complex |
| Privacy | Cloud | Cloud | Local |
| Customization | Limited | Limited | High |

## 🛠️ Advanced Usage

### Run Setup Guide
```bash
python SETUP.py
```

### Run Demo & Tests
```bash
python demo.py
```

### Enable Debug Mode
Edit `.env`:
```bash
DEBUG=True
LOG_LEVEL=DEBUG
```

### Use Different Model
Edit `.env`:
```bash
# For Ollama users
MODEL_NAME=llama3.2
# or
MODEL_NAME=mistral
```

## 📚 Learning Resources

### Cybersecurity Frameworks
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)
- [MITRE ATT&CK Framework](https://attack.mitre.org/)
- [CIS Top 18 Controls](https://www.cisecurity.org/cis-controls)
- [ISO 27001 Controls](https://www.iso.org/isoiec-27001-information-security-management.html)

### Certifications Covered
- Security+ (CompTIA)
- CEH (Certified Ethical Hacker)
- CISSP (ISC²)
- CySA+ (CompTIA)
- Cloud Security (AWS, Azure, GCP)

### Sample Questions to Try
```
Explain zero-day vulnerabilities
What's the difference between IDS and IPS?
How do I implement defense in depth?
Explain the shared responsibility model in cloud
What are the STRIDE threat modeling techniques?
How to respond to a ransomware incident?
What is threat hunting?
Explain the kill chain framework
```

## 🐛 Troubleshooting

### "API Key Invalid"
- Check your `.env` file
- Verify API key has no extra spaces
- Ensure key is correct for the provider

### "Ollama runner process terminated"
- Your system may not have enough RAM
- Try a smaller model: `neural-chat` instead of `llama3.2`
- Ensure Ollama server is running: `ollama serve`
- Check available memory: `free -h`

### "Cannot connect to Ollama"
- Start Ollama: `ollama serve`
- Check it's running: `ollama list`
- Verify OLLAMA_HOST in `.env` matches actual host

### "PyAudio not found" (Voice features)
In a container or headless environment, voice is disabled - this is normal.

### "libespeak error" (Voice output)
Text-to-speech requires system audio libraries - not available in all environments.

## 📦 Dependencies

**Core:**
- python-dotenv: Environment config
- rich: Beautiful terminal output
- click: CLI interface
- pydantic: Data validation

**LLM Integrations:**
- openai: OpenAI API
- anthropic: Anthropic Claude API
- ollama: Local Ollama models

**Voice (Optional):**
- SpeechRecognition: Audio input
- pyttsx3: Text-to-speech
- gTTS: Google Text-to-Speech
- playsound: Audio playback

**Data & ML:**
- numpy: Numerical computing
- pandas: Data analysis
- gradio: Web UI (optional)

## 📄 License

MIT License - See LICENSE file for details

## 🤝 Contributing

Contributions welcome! Areas for enhancement:
- Additional cybersecurity knowledge base
- More LLM provider support
- Web UI improvements
- Offline mode enhancements

## 📧 Support

For issues:
1. Check `.env` configuration
2. Review error messages carefully
3. Try the setup guide: `python SETUP.py`
4. Check the relevant LLM provider's documentation

---

**Happy Learning! 🕷️** Stay secure and keep learning cybersecurity!
