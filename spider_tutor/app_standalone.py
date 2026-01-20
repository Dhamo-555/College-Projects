#!/usr/bin/env python3
"""
🕷️ Spider - Cybersecurity Tutor
All-in-one Gradio app for permanent HuggingFace Spaces deployment
Mobile and Desktop responsive
"""

import gradio as gr
import os

# Try to import with fallback
try:
    from modules.knowledge_base import knowledge_base
    from modules.ai_engine import AIEngine
    from modules.safety import check_safety
    from config import settings, SYSTEM_PROMPT
    MODULES_AVAILABLE = True
except:
    MODULES_AVAILABLE = False
    print("⚠️  Running in demo mode - some features limited")

# Initialize AI Engine if available
ai_engine = None

def get_ai_engine():
    global ai_engine
    if ai_engine is None and MODULES_AVAILABLE:
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
# Chat Functions
# ============================================================================

def chat_interface(message: str, chat_history):
    """Chat interface"""
    if not message.strip():
        return "", chat_history
    
    try:
        if not MODULES_AVAILABLE:
            response = f"Demo Response to: {message}\n\nFor full functionality, please ensure all modules are installed."
        else:
            is_safe, safety_msg = check_safety(message)
            if not is_safe:
                return "", chat_history
            
            ai = get_ai_engine()
            response = ai.chat(message, stream=False)
        
        chat_history.append((message, response))
        return "", chat_history
    except Exception as e:
        chat_history.append((message, f"❌ Error: {str(e)}"))
        return "", chat_history

def get_flashcard():
    """Get random flashcard"""
    if not MODULES_AVAILABLE:
        return "### 🎴 Demo Flashcard\n\n**Q:** What is the CIA triad?\n\n**A:** Confidentiality, Integrity, Availability"
    
    try:
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
    except Exception as e:
        return f"❌ Error: {str(e)}"

def generate_quiz(count: int):
    """Generate quiz"""
    if not MODULES_AVAILABLE:
        return "### 📝 Demo Quiz\n\n**Q1:** What does CIA stand for?\n\n**A:** Confidentiality, Integrity, Availability"
    
    try:
        quiz = knowledge_base.get_quiz(count=count)
        output = "### 📝 Quiz Questions\n\n"
        for i, q in enumerate(quiz, 1):
            output += f"**Q{i}:** {q.get('question', 'N/A')}\n\n"
            output += f"*Answer:* {q.get('answer', 'N/A')}\n\n---\n\n"
        return output
    except Exception as e:
        return f"❌ Error: {str(e)}"

def search_mitre(tech_id: str):
    """Search MITRE ATT&CK"""
    if not tech_id.strip():
        return "❌ Please enter a technique ID"
    
    if not MODULES_AVAILABLE:
        return f"### Demo MITRE Lookup: {tech_id}\n\nFor full MITRE database access, ensure all modules are installed."
    
    try:
        tech_id = tech_id.strip().upper()
        if not tech_id.startswith("T"):
            tech_id = "T" + tech_id
        
        tech = knowledge_base.get_mitre_technique(tech_id)
        if tech:
            return f"### {tech.technique_id}: {tech.name}\n\n{getattr(tech, 'description', 'N/A')}"
        
        results = knowledge_base.search_mitre(tech_id.replace("T", ""))
        if results:
            output = f"Found {len(results)} techniques:\n\n"
            for r in results:
                output += f"• **{r.technique_id}: {r.name}**\n"
            return output
        
        return f"❌ Technique '{tech_id}' not found"
    except Exception as e:
        return f"❌ Error: {str(e)}"

def get_incident_template():
    """Get incident template"""
    if not MODULES_AVAILABLE:
        return "### Incident Report Template\n\n**Date:** ___\n**Reporter:** ___\n**Severity:** ___\n\n**Description:**\n\n**Timeline:**\n\n**Impact:**\n\n**Remediation:**"
    
    try:
        return knowledge_base.get_incident_template()
    except Exception as e:
        return f"❌ Error: {str(e)}"

def get_vuln_template():
    """Get vulnerability template"""
    if not MODULES_AVAILABLE:
        return "### Vulnerability Report Template\n\n**Title:** ___\n**CVSS Score:** ___\n\n**Description:**\n\n**Affected Systems:**\n\n**Remediation:**"
    
    try:
        return knowledge_base.get_vulnerability_template()
    except Exception as e:
        return f"❌ Error: {str(e)}"

def get_checklist(system_type: str):
    """Get hardening checklist"""
    if not MODULES_AVAILABLE:
        return f"### {system_type.title()} Hardening Checklist\n\n☐ Update system\n☐ Enable firewall\n☐ Configure permissions\n☐ Enable logging\n☐ Set password policy"
    
    try:
        return knowledge_base.get_hardening_checklist(system_type.lower())
    except Exception as e:
        return f"❌ Error: {str(e)}"

# ============================================================================
# Create Gradio Interface
# ============================================================================

with gr.Blocks(
    title="🕷️ Spider - Cybersecurity Tutor",
    theme=gr.themes.Soft(),
    css="""
        @media (max-width: 768px) {
            .gradio-container {
                max-width: 100% !important;
                padding: 10px !important;
            }
            
            .gradio-block {
                padding: 10px !important;
            }
            
            .gradio-textbox, textarea {
                font-size: 16px !important;
            }
            
            .gradio-button {
                font-size: 14px !important;
                padding: 8px !important;
            }
            
            .gradio-slider, .gradio-radio {
                margin: 10px 0 !important;
            }
            
            h1, h2, h3 {
                font-size: 1.2em !important;
            }
        }
        
        @media (max-width: 480px) {
            .gradio-container {
                padding: 5px !important;
            }
            
            h1 { font-size: 1em !important; }
            h2 { font-size: 0.95em !important; }
            
            .gradio-tabs {
                overflow-x: auto !important;
            }
        }
        
        .gradio-chatbot {
            min-height: 400px !important;
        }
        
        @media (max-width: 768px) {
            .gradio-chatbot {
                min-height: 300px !important;
            }
        }
    """
) as demo:
    
    # Header
    gr.Markdown("""
    # 🕷️ Spider - AI-Powered Cybersecurity Tutor
    
    Your friendly learning companion for cybersecurity education.
    **Fully responsive on mobile and desktop** 📱💻
    """)
    
    # ====== Chat Tab ======
    with gr.Tab("💬 Chat"):
        gr.Markdown("Ask any cybersecurity question - AI powered responses!")
        
        with gr.Row():
            chatbot = gr.Chatbot(label="🤖 Spider Chat", height=400)
        
        with gr.Row():
            message = gr.Textbox(placeholder="Ask a cybersecurity question...", lines=2)
        
        message.submit(
            chat_interface,
            inputs=[message, chatbot],
            outputs=[message, chatbot]
        )
    
    # ====== Flashcards Tab ======
    with gr.Tab("🎴 Flashcards"):
        gr.Markdown("Study with random cybersecurity flashcards")
        
        btn = gr.Button("Get Random Flashcard")
        output = gr.Markdown()
        
        btn.click(get_flashcard, outputs=output)
    
    # ====== Quiz Tab ======
    with gr.Tab("📝 Quiz"):
        gr.Markdown("Test your cybersecurity knowledge")
        
        count = gr.Slider(1, 20, value=5, label="Number of Questions")
        btn = gr.Button("Generate Quiz")
        output = gr.Markdown()
        
        btn.click(generate_quiz, inputs=count, outputs=output)
    
    # ====== MITRE Tab ======
    with gr.Tab("🎯 MITRE ATT&CK"):
        gr.Markdown("Look up MITRE ATT&CK techniques")
        
        tech_id = gr.Textbox(placeholder="T1566 or keyword", label="Technique ID/Keyword")
        btn = gr.Button("Search")
        output = gr.Markdown()
        
        btn.click(search_mitre, inputs=tech_id, outputs=output)
    
    # ====== Templates Tab ======
    with gr.Tab("📋 Templates"):
        gr.Markdown("Security report templates")
        
        incident_btn = gr.Button("Incident Template")
        vuln_btn = gr.Button("Vulnerability Template")
        output = gr.Markdown()
        
        incident_btn.click(get_incident_template, outputs=output)
        vuln_btn.click(get_vuln_template, outputs=output)
    
    # ====== Checklist Tab ======
    with gr.Tab("✅ Hardening"):
        gr.Markdown("Security hardening checklists")
        
        system = gr.Radio(
            ["General", "Linux", "Windows", "Network"],
            value="General",
            label="System Type"
        )
        btn = gr.Button("Get Checklist")
        output = gr.Markdown()
        
        btn.click(lambda x: get_checklist(x), inputs=system, outputs=output)
    
    # ====== About Tab ======
    with gr.Tab("ℹ️ About"):
        gr.Markdown("""
        ## About Spider Tutor
        
        Spider is an AI-powered cybersecurity learning platform.
        
        ### Features
        - 💬 AI Chat - Instant cybersecurity guidance
        - 🎴 Flashcards - Study mode
        - 📝 Quizzes - Test knowledge
        - 🎯 MITRE ATT&CK - Technique lookup
        - 📋 Templates - Report templates
        - ✅ Checklists - Hardening guides
        
        ### Device Support
        ✅ Mobile (iOS, Android)
        ✅ Tablet
        ✅ Desktop (Windows, Mac, Linux)
        
        ### Created by
        **Dhamodharaprashad**
        
        Stay secure! 🔒
        """)

if __name__ == "__main__":
    demo.launch(
        share=False,
        show_error=True,
        server_name="0.0.0.0",
        server_port=7860
    )
