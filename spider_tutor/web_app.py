#!/usr/bin/env python3
"""
🕷️ Spider - Beautiful Web Interface
FastAPI + Custom HTML/CSS
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
from typing import Optional
import json
import os

# Import core modules
from config import settings, SYSTEM_PROMPT
from modules.ai_engine import AIEngine
from modules.safety import check_safety
from modules.knowledge_base import knowledge_base

# ============================================================================
# FastAPI Setup
# ============================================================================

app = FastAPI(title="🕷️ Spider - Cybersecurity Tutor")

# Initialize AI Engine (lazy)
ai_engine = None

def get_ai_engine():
    global ai_engine
    if ai_engine is None:
        api_key = None
        if settings.llm_provider == "openai":
            api_key = settings.openai_api_key
        elif settings.llm_provider == "anthropic":
            api_key = settings.anthropic_api_key
        
        ai_engine = AIEngine(
            provider=settings.llm_provider,
            api_key=api_key,
            model=settings.model_name,
            max_tokens=settings.max_tokens,
            temperature=settings.temperature,
            system_prompt=SYSTEM_PROMPT
        )
    return ai_engine

# ============================================================================
# Models
# ============================================================================

class ChatMessage(BaseModel):
    message: str

class QuizRequest(BaseModel):
    count: int = 5

class MitreRequest(BaseModel):
    tech_id: str

# ============================================================================
# Routes
# ============================================================================

@app.get("/")
async def index():
    """Serve main HTML page"""
    return FileResponse("templates/index.html", media_type="text/html")

@app.post("/api/chat")
async def chat(data: ChatMessage):
    """Chat endpoint"""
    try:
        # Safety check
        is_safe, safety_message = check_safety(data.message)
        if not is_safe:
            return JSONResponse({"error": safety_message}, status_code=400)
        
        # Get response
        ai = get_ai_engine()
        response = ai.chat(data.message, stream=False)
        
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/flashcard")
async def get_flashcard():
    """Get random flashcard"""
    try:
        cards = knowledge_base.get_flashcards(count=1)
        if cards:
            card = cards[0]
            return {
                "question": card.question,
                "answer": card.answer,
                "category": card.category,
                "difficulty": card.difficulty
            }
        return {"error": "No flashcards available"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/quiz")
async def get_quiz(data: QuizRequest):
    """Get quiz questions"""
    try:
        quiz = knowledge_base.get_quiz(count=data.count)
        questions = []
        for q in quiz:
            questions.append({
                "question": q.get("question", ""),
                "answer": q.get("answer", "")
            })
        return {"questions": questions}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/mitre")
async def search_mitre(data: MitreRequest):
    """Search MITRE ATT&CK"""
    try:
        tech_id = data.tech_id.strip().upper()
        if not tech_id.startswith("T"):
            tech_id = "T" + tech_id
        
        tech = knowledge_base.get_mitre_technique(tech_id)
        if tech:
            return {
                "id": tech.technique_id,
                "name": tech.name,
                "description": getattr(tech, "description", "N/A")
            }
        
        # Try searching
        results = knowledge_base.search_mitre(tech_id.replace("T", ""))
        if results:
            return {
                "results": [
                    {"id": t.technique_id, "name": t.name}
                    for t in results
                ]
            }
        
        return {"error": f"Technique '{tech_id}' not found"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/incident-template")
async def incident_template():
    """Get incident template"""
    try:
        template = knowledge_base.get_incident_template()
        return {"template": template}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/vuln-template")
async def vuln_template():
    """Get vulnerability template"""
    try:
        template = knowledge_base.get_vulnerability_template()
        return {"template": template}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/checklist/{system_type}")
async def get_checklist(system_type: str = "general"):
    """Get hardening checklist"""
    try:
        checklist = knowledge_base.get_hardening_checklist(system_type)
        return {"checklist": checklist}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health():
    """Health check"""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
