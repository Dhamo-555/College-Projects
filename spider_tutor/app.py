#!/usr/bin/env python3
"""
🕷️ Spider - Web Interface with Gradio
Deployment-ready web application
"""

import gradio as gr
from typing import Optional
import sys

# Import configuration
from config import settings, SYSTEM_PROMPT

# Import modules
from modules.ai_engine import AIEngine
from modules.safety import check_safety
from modules.knowledge_base import knowledge_base

# Initialize AI Engine
def init_ai():
    """Initialize AI Engine"""
    api_key = None
    if settings.llm_provider == "openai":
        api_key = settings.openai_api_key
    elif settings.llm_provider == "anthropic":
        api_key = settings.anthropic_api_key
    
    return AIEngine(
        provider=settings.llm_provider,
        api_key=api_key,
        model=settings.model_name,
        max_tokens=settings.max_tokens,
        temperature=settings.temperature,
        system_prompt=SYSTEM_PROMPT
    )

# Global AI instance - initialize lazily
ai_engine = None
conversation_history = []

def get_ai_engine():
    global ai_engine
    if ai_engine is None:
        ai_engine = init_ai()
    return ai_engine

# ============================================================================
# Chat Functions
# ============================================================================

def chat_with_spider(message: str, chat_history: list) -> tuple[str, list]:
    """Process user message and return AI response"""
    global conversation_history
    
    # Safety check
    is_safe, safety_message = check_safety(message)
    if not is_safe:
        return safety_message, chat_history
    
    try:
        # Get AI engine
        ai = get_ai_engine()
        
        # Get AI response
        response = ai.chat(message, stream=False)
        
        # Update chat history
        chat_history.append((message, response))
        
        return response, chat_history
    
    except Exception as e:
        error_msg = f"❌ Error: {str(e)}"
        chat_history.append((message, error_msg))
        return error_msg, chat_history

# ============================================================================
# Knowledge Base Functions
# ============================================================================

def get_random_flashcard() -> str:
    """Get a random flashcard"""
    cards = knowledge_base.get_flashcards(count=1)
    if cards:
        card = cards[0]
        return f"""
### 🎴 Flashcard

**Question:** {card.question}

**Answer:** {card.answer}

**Category:** {card.category} | **Difficulty:** {card.difficulty}
        """
    return "No flashcards available"

def get_quiz_questions(num_questions: int = 5) -> str:
    """Get quiz questions"""
    quiz = knowledge_base.get_quiz(count=num_questions)
    return knowledge_base.format_quiz(quiz, show_answers=False)

def get_quiz_answers(num_questions: int = 5) -> str:
    """Get quiz answers"""
    quiz = knowledge_base.get_quiz(count=num_questions)
    return knowledge_base.format_quiz(quiz, show_answers=True)

def search_mitre(tech_id: str) -> str:
    """Search MITRE ATT&CK technique"""
    if not tech_id:
        return "Please enter a technique ID (e.g., T1566)"
    
    tech_id = tech_id.strip().upper()
    if not tech_id.startswith("T"):
        tech_id = "T" + tech_id
    
    tech = knowledge_base.get_mitre_technique(tech_id)
    if tech:
        return knowledge_base.format_mitre_technique(tech)
    
    # Try searching
    results = knowledge_base.search_mitre(tech_id.replace("T", ""))
    if results:
        output = f"Found {len(results)} techniques:\n\n"
        for t in results:
            output += f"• **{t.technique_id}: {t.name}**\n"
        return output
    
    return f"❌ Technique '{tech_id}' not found"

def get_incident_template() -> str:
    """Get incident report template"""
    return knowledge_base.get_incident_template()

def get_vuln_template() -> str:
    """Get vulnerability report template"""
    return knowledge_base.get_vulnerability_template()

def get_hardening_checklist(system_type: str = "general") -> str:
    """Get hardening checklist"""
    return knowledge_base.get_hardening_checklist(system_type)

# ============================================================================
# Gradio Interface
# ============================================================================

def create_interface():
    """Create Gradio interface"""
    
    with gr.Blocks(title="🕷️ Spider - Cybersecurity Tutor", theme=gr.themes.Soft()) as demo:
        
        # Header
        gr.Markdown("""
        # 🕷️ Spider - AI-Powered Cybersecurity Tutor
        
        Your friendly voice-enabled cybersecurity learning companion. Ask questions, 
        get insights from MITRE ATT&CK, access templates, and more!
        """)
        
        # ====== Main Chat Tab ======
        with gr.Tab("💬 Chat"):
            gr.Markdown("Ask any cybersecurity question and get instant answers from Spider!")
            
            chatbot = gr.Chatbot(
                label="Spider Chat",
                height=500,
                show_copy_button=True
            )
            
            with gr.Row():
                user_input = gr.Textbox(
                    placeholder="Ask a cybersecurity question...",
                    label="Your Question",
                    scale=4
                )
                submit_btn = gr.Button("Send", scale=1)
            
            # Submit handler
            def submit_message(message, history):
                return chat_with_spider(message, history)
            
            submit_btn.click(
                submit_message,
                inputs=[user_input, chatbot],
                outputs=[user_input, chatbot]
            )
            
            user_input.submit(
                submit_message,
                inputs=[user_input, chatbot],
                outputs=[user_input, chatbot]
            )
        
        # ====== Flashcard Tab ======
        with gr.Tab("🎴 Flashcards"):
            gr.Markdown("Study with random cybersecurity flashcards")
            
            flashcard_output = gr.Markdown()
            flashcard_btn = gr.Button("Get Random Flashcard")
            flashcard_btn.click(
                get_random_flashcard,
                outputs=flashcard_output
            )
        
        # ====== Quiz Tab ======
        with gr.Tab("📝 Quiz"):
            gr.Markdown("Test your cybersecurity knowledge")
            
            with gr.Row():
                num_questions = gr.Slider(
                    minimum=1,
                    maximum=20,
                    value=5,
                    step=1,
                    label="Number of Questions"
                )
            
            quiz_output = gr.Markdown()
            
            with gr.Row():
                quiz_btn = gr.Button("Generate Quiz")
                answers_btn = gr.Button("Show Answers")
            
            quiz_btn.click(
                get_quiz_questions,
                inputs=num_questions,
                outputs=quiz_output
            )
            
            answers_btn.click(
                get_quiz_answers,
                inputs=num_questions,
                outputs=quiz_output
            )
        
        # ====== MITRE ATT&CK Tab ======
        with gr.Tab("🎯 MITRE ATT&CK"):
            gr.Markdown("Look up MITRE ATT&CK techniques")
            
            with gr.Row():
                mitre_input = gr.Textbox(
                    placeholder="T1566 or search keyword",
                    label="Technique ID or Keyword",
                    scale=4
                )
                mitre_btn = gr.Button("Search", scale=1)
            
            mitre_output = gr.Markdown()
            
            mitre_btn.click(
                search_mitre,
                inputs=mitre_input,
                outputs=mitre_output
            )
            
            mitre_input.submit(
                search_mitre,
                inputs=mitre_input,
                outputs=mitre_output
            )
        
        # ====== Templates Tab ======
        with gr.Tab("📋 Templates"):
            gr.Markdown("Get incident and vulnerability report templates")
            
            with gr.Row():
                incident_btn = gr.Button("Incident Report Template")
                vuln_btn = gr.Button("Vulnerability Report Template")
            
            template_output = gr.Markdown()
            
            incident_btn.click(
                get_incident_template,
                outputs=template_output
            )
            
            vuln_btn.click(
                get_vuln_template,
                outputs=template_output
            )
        
        # ====== Hardening Checklist Tab ======
        with gr.Tab("✅ Hardening Checklist"):
            gr.Markdown("Get security hardening checklists for different systems")
            
            system_type = gr.Radio(
                choices=["general", "linux", "windows", "network"],
                value="general",
                label="Select System Type"
            )
            
            checklist_btn = gr.Button("Get Checklist")
            checklist_output = gr.Markdown()
            
            checklist_btn.click(
                get_hardening_checklist,
                inputs=system_type,
                outputs=checklist_output
            )
        
        # ====== About Tab ======
        with gr.Tab("ℹ️ About"):
            gr.Markdown("""
            ## About Spider Tutor
            
            Spider is an AI-powered cybersecurity tutor that helps you learn and understand
            cybersecurity concepts, MITRE ATT&CK framework, security best practices, and more.
            
            ### Features
            - 💬 Interactive AI chat with cybersecurity expertise
            - 🎴 Flashcards for studying
            - 📝 Quiz questions to test your knowledge
            - 🎯 MITRE ATT&CK framework lookup
            - 📋 Security report templates
            - ✅ Hardening checklists
            
            ### LLM Providers
            - OpenAI GPT-4o-mini (Recommended)
            - Anthropic Claude
            - Ollama (Local, offline)
            
            ### Created by
            **Dhamodharaprashad**
            
            ---
            
            **Note:** Keep your API keys secure. Never share them publicly.
            """)
    
    return demo

if __name__ == "__main__":
    demo = create_interface()
    
    # Launch with public sharing
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=True,
        show_error=True
    )
