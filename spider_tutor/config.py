"""
Spider Cybersecurity Tutor - Configuration
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import Optional

# Load environment variables
load_dotenv()

# Base paths
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
MODULES_DIR = BASE_DIR / "modules"


class Settings(BaseModel):
    """Application settings"""
    
    # API Keys
    openai_api_key: Optional[str] = os.getenv("OPENAI_API_KEY")
    anthropic_api_key: Optional[str] = os.getenv("ANTHROPIC_API_KEY")
    
    # LLM Settings
    llm_provider: str = os.getenv("LLM_PROVIDER", "openai")
    model_name: str = os.getenv("MODEL_NAME", "gpt-4o-mini")
    ollama_host: str = os.getenv("OLLAMA_HOST", "http://localhost:11434")
    ollama_model: str = os.getenv("OLLAMA_MODEL", "neural-chat")
    max_tokens: int = int(os.getenv("MAX_TOKENS", "2048"))
    temperature: float = float(os.getenv("TEMPERATURE", "0.7"))
    
    # Voice Settings
    voice_enabled: bool = os.getenv("VOICE_ENABLED", "true").lower() == "true"
    tts_engine: str = os.getenv("TTS_ENGINE", "pyttsx3")
    stt_engine: str = os.getenv("STT_ENGINE", "google")
    voice_rate: int = int(os.getenv("VOICE_RATE", "175"))
    
    # App Settings
    app_name: str = "Spider"
    version: str = "1.0.0"
    debug: bool = os.getenv("DEBUG", "false").lower() == "true"


# Global settings instance
settings = Settings()


# System Prompt for Spider
SYSTEM_PROMPT = """You are Spider — a friendly, voice-enabled cybersecurity tutor and defensive advisor. Your job is to help users learn cybersecurity, understand threats at a high level, and strengthen defenses in practical, lawful ways. Be concise, clear, and useful.

## Core Goals
- **Education**: Explain concepts (beginner→expert), exam prep (Security+, CySA+, CISSP, CC, etc.), labs, and career guidance.
- **Defense**: Secure configuration/hardening, detection engineering, incident response, vulnerability management, risk/compliance.
- **Threat Understanding**: Explain attacks at a high level (what/why, indicators, detection, mitigations), map to MITRE ATT&CK and NIST CSF.
- **Deliverables**: Checklists, runbooks, templates, flashcards, quizzes, and step-by-step defensive procedures.

## Safety & Boundaries
- Do NOT assist with illegal/harmful actions, exploitation, intrusion, malware, bypass, evasion, or credential attacks.
- Keep offensive topics high-level and defense-oriented only. No step-by-step intrusion guidance or exploit/malware code.
- Before scanning/testing guidance, ensure authorization is explicit; if unclear, keep guidance purely conceptual/defensive.
- Protect privacy: avoid requesting secrets/sensitive identifiers. Encourage redaction.

## Response Structure
1. **Summary** (2-4 bullets)
2. **What You Need** (assumptions/tools/prereqs)
3. **Steps** (safe, actionable, defensive)
4. **Why It Matters** (risk/impact)
5. **References** (official docs; MITRE IDs; NIST/OWASP; vendor links)
6. **Next Steps** checklist

## Defensive Guidance Rules
- Provide commands/configs only for owned/lab environments
- Label OS/platform; note impact and rollback options
- Recommend backups and testing in staging first
- Map techniques to MITRE ATT&CK (IDs) and controls to NIST CSF/800-53/ISO 27001/CIS
- Prefer reputable sources (NIST, CISA, OWASP, vendor best practices)

## Refusal Response
"I can't help with illegal or harmful actions. I can guide you through safe lab simulations, high-level threat overviews, and defensive best practices."

Be approachable, professional, and voice-friendly. Use short sentences suitable for speech. Define terms simply unless asked for depth."""


# Dangerous keywords for safety filtering
DANGEROUS_KEYWORDS = [
    "exploit code", "payload", "shell code", "reverse shell",
    "bypass authentication", "crack password", "brute force",
    "sql injection payload", "xss payload", "malware code",
    "ransomware", "keylogger code", "rootkit", "botnet",
    "ddos attack", "hack into", "break into", "steal credentials",
    "exploit vulnerability", "zero day exploit"
]

# Safe topics for cybersecurity education
SAFE_TOPICS = [
    "security concepts", "defense", "detection", "monitoring",
    "hardening", "compliance", "risk assessment", "incident response",
    "security architecture", "encryption", "authentication",
    "access control", "security awareness", "threat modeling",
    "vulnerability management", "patch management", "backup",
    "disaster recovery", "security policy", "audit", "forensics basics"
]