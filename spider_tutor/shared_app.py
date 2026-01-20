#!/usr/bin/env python3
"""
🕷️ Spider - Shared Public App
Uses Gradio's sharing mechanism with FastAPI backend
"""

import gradio as gr
import requests
import json
from typing import List, Tuple

# Configuration
API_URL = "http://localhost:8000"

# ============================================================================
# Gradio Interface Components
# ============================================================================

def chat_interface(message: str, chat_history: List[Tuple[str, str]]) -> Tuple[str, List[Tuple[str, str]]]:
    """Chat interface"""
    if not message.strip():
        return "", chat_history
    
    try:
        response = requests.post(f"{API_URL}/api/chat", json={"message": message})
        if response.status_code == 200:
            data = response.json()
            bot_message = data.get("response", "No response")
            chat_history.append((message, bot_message))
            return "", chat_history
        else:
            error = response.json().get("detail", "Error")
            chat_history.append((message, f"❌ Error: {error}"))
            return "", chat_history
    except Exception as e:
        chat_history.append((message, f"❌ Error: {str(e)}"))
        return "", chat_history

def get_flashcard():
    """Get random flashcard"""
    try:
        response = requests.get(f"{API_URL}/api/flashcard")
        if response.status_code == 200:
            data = response.json()
            return f"""
### 🎴 Flashcard

**Question:** {data['question']}

**Answer:** {data['answer']}

**Category:** {data['category']} | **Difficulty:** {data['difficulty']}
            """
        else:
            return "❌ Error loading flashcard"
    except Exception as e:
        return f"❌ Error: {str(e)}"

def generate_quiz(count: int):
    """Generate quiz"""
    try:
        response = requests.post(f"{API_URL}/api/quiz", json={"count": count})
        if response.status_code == 200:
            data = response.json()
            output = "### 📝 Quiz Questions\n\n"
            for i, q in enumerate(data['questions'], 1):
                output += f"**Q{i}:** {q['question']}\n\n"
                output += f"*Answer:* {q['answer']}\n\n---\n\n"
            return output
        else:
            return "❌ Error generating quiz"
    except Exception as e:
        return f"❌ Error: {str(e)}"

def search_mitre(tech_id: str):
    """Search MITRE ATT&CK"""
    if not tech_id.strip():
        return "❌ Please enter a technique ID"
    
    try:
        response = requests.post(f"{API_URL}/api/mitre", json={"tech_id": tech_id})
        if response.status_code == 200:
            data = response.json()
            if "results" in data:
                output = f"Found {len(data['results'])} techniques:\n\n"
                for r in data['results']:
                    output += f"• **{r['id']}: {r['name']}**\n"
                return output
            else:
                return f"### {data['id']}: {data['name']}\n\n{data['description']}"
        else:
            return f"❌ {response.json().get('error', 'Error')}"
    except Exception as e:
        return f"❌ Error: {str(e)}"

def get_incident_template():
    """Get incident template"""
    try:
        response = requests.get(f"{API_URL}/api/incident-template")
        if response.status_code == 200:
            data = response.json()
            return data['template']
        else:
            return "❌ Error loading template"
    except Exception as e:
        return f"❌ Error: {str(e)}"

def get_vuln_template():
    """Get vulnerability template"""
    try:
        response = requests.get(f"{API_URL}/api/vuln-template")
        if response.status_code == 200:
            data = response.json()
            return data['template']
        else:
            return "❌ Error loading template"
    except Exception as e:
        return f"❌ Error: {str(e)}"

def get_checklist(system_type: str):
    """Get hardening checklist"""
    try:
        response = requests.get(f"{API_URL}/api/checklist/{system_type}")
        if response.status_code == 200:
            data = response.json()
            return data['checklist']
        else:
            return "❌ Error loading checklist"
    except Exception as e:
        return f"❌ Error: {str(e)}"

# ============================================================================
# Create Gradio Interface
# ============================================================================

def create_interface():
    """Create the Gradio interface"""
    
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
                
                .gradio-textbox {
                    font-size: 16px !important;
                }
                
                .gradio-button {
                    font-size: 14px !important;
                    padding: 8px !important;
                }
                
                .gradio-slider {
                    margin: 10px 0 !important;
                }
                
                .gradio-radio {
                    font-size: 14px !important;
                }
                
                .gradio-markdown {
                    font-size: 14px !important;
                }
                
                textarea {
                    font-size: 16px !important;
                    padding: 10px !important;
                }
            }
            
            @media (max-width: 480px) {
                .gradio-container {
                    max-width: 100% !important;
                    padding: 5px !important;
                }
                
                h1, h2, h3 {
                    font-size: 1.2em !important;
                }
                
                .gradio-tabs {
                    overflow-x: auto !important;
                }
                
                .gradio-tab {
                    padding: 8px !important;
                    font-size: 12px !important;
                }
            }
            
            body {
                font-size: 14px;
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
        
        Your friendly AI learning companion for cybersecurity. Ask questions, study flashcards, 
        take quizzes, and explore MITRE ATT&CK techniques!
        """)
        
        # ====== Chat Tab ======
        with gr.Tab("💬 Chat"):
            gr.Markdown("Ask any cybersecurity question and get instant AI responses!")
            
            with gr.Row():
                chatbot = gr.Chatbot(label="🤖 Spider Chat", height=500)
            
            with gr.Row():
                message = gr.Textbox(placeholder="Ask a cybersecurity question...")
            
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
            gr.Markdown("Get security report templates")
            
            incident_btn = gr.Button("Incident Template")
            vuln_btn = gr.Button("Vulnerability Template")
            output = gr.Markdown()
            
            incident_btn.click(get_incident_template, outputs=output)
            vuln_btn.click(get_vuln_template, outputs=output)
        
        # ====== Checklist Tab ======
        with gr.Tab("✅ Hardening Checklists"):
            gr.Markdown("Get security hardening checklists")
            
            with gr.Row():
                system = gr.Radio(
                    ["General", "Linux", "Windows", "Network"],
                    value="General",
                    label="System Type"
                )
                btn = gr.Button("Get Checklist")
            
            output = gr.Markdown()
            
            btn.click(
                lambda x: get_checklist(x.lower()),
                inputs=system,
                outputs=output
            )
        
        # ====== About Tab ======
        with gr.Tab("ℹ️ About"):
            gr.Markdown("""
            ## About Spider Tutor
            
            Spider is an AI-powered cybersecurity tutor helping you learn:
            - Cybersecurity concepts & best practices
            - MITRE ATT&CK framework
            - Security hardening techniques
            - Incident response procedures
            
            ### Features
            - 🤖 AI-powered responses
            - 🎴 Flashcards for studying
            - 📝 Quiz questions
            - 🎯 MITRE ATT&CK lookup
            - 📋 Security templates
            - ✅ Hardening checklists
            
            ### Created by
            **Dhamodharaprashad** 
            
            Stay secure! 🔒
            """)
    
    return demo

if __name__ == "__main__":
    # Wait for FastAPI to be ready
    import time
    print("⏳ Waiting for API to be ready...")
    for i in range(30):
        try:
            requests.get(f"{API_URL}/health")
            print("✅ API is ready!")
            break
        except:
            time.sleep(1)
    
    print("🚀 Starting Gradio interface with public sharing...")
    demo = create_interface()
    demo.launch(
        share=True,
        show_error=True,
        server_name="0.0.0.0",
        server_port=7860
    )
