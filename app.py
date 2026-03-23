"""
Streamlit app for the Agentic AI Security System.
Provides a ChatGPT-like web interface for secure AI interactions.
"""

import streamlit as st
from workflow import get_workflow

# Configure page
st.set_page_config(
    page_title="Agentic AI Security System",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main {
        padding: 0;
    }
    .stChatMessage {
        padding: 1rem 0;
    }
    .chatbot-container {
        max-width: 900px;
        margin: 0 auto;
        padding: 2rem 1rem;
    }
    .input-container {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background: linear-gradient(to top, rgba(255,255,255,1), rgba(255,255,255,0.95));
        padding: 1rem 0;
        border-top: 1px solid #e5e5e5;
        z-index: 100;
    }
    .chat-bubble {
        border-radius: 12px;
        padding: 12px 16px;
        margin: 8px 0;
    }
    .user-bubble {
        background: #10a37f;
        color: white;
        margin-left: auto;
        max-width: 80%;
    }
    .assistant-bubble {
        background: #f7f7f7;
        color: black;
        margin-right: auto;
        max-width: 80%;
        border: 1px solid #e5e5e5;
    }
    .security-warning {
        background: #fff4e6;
        border-left: 4px solid #ff9800;
        padding: 12px;
        border-radius: 4px;
        margin: 8px 0;
    }
    .security-safe {
        background: #f1f8e9;
        border-left: 4px solid #4caf50;
        padding: 12px;
        border-radius: 4px;
        margin: 8px 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
if "processed_input" not in st.session_state:
    st.session_state.processed_input = None

def main():
    # Header
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<h1 style='text-align: center; color: #10a37f;'>🤖 Agentic Security AI</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #666;'>A ChatGPT-like AI with advanced security threat detection</p>", unsafe_allow_html=True)

    # Display chat history with better styling
    st.markdown("<div class='chatbot-container'>", unsafe_allow_html=True)
    
    for message in st.session_state.messages:
        if message["role"] == "user":
            col1, col2 = st.columns([1, 4])
            with col2:
                st.markdown(f"<div style='background: #10a37f; color: white; border-radius: 12px; padding: 12px 16px; margin: 8px 0;'><strong>You:</strong> {message['content']}</div>", unsafe_allow_html=True)
        else:
            col1, col2 = st.columns([4, 1])
            with col1:
                st.markdown(f"<div style='background: #f7f7f7; color: black; border-radius: 12px; padding: 12px 16px; margin: 8px 0; border: 1px solid #e5e5e5;'><strong>🤖 Assistant:</strong><br/>{message['content']}</div>", unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

    # Add spacing for fixed input
    st.markdown("<br>" * 4, unsafe_allow_html=True)

    # Chat input at the bottom
    with st.markdown("<div class='input-container'>", unsafe_allow_html=True):
        col1, col2, col3 = st.columns([0.5, 8, 0.5])
        
        with col2:
            with st.form(key="chat_form", clear_on_submit=True):
                prompt = st.text_input(
                    "💬",
                    placeholder="Ask me anything... (I'll also check for security threats)",
                    label_visibility="collapsed"
                )
                submitted = st.form_submit_button("Send", use_container_width=False)
        
        if submitted and prompt:
            # Add user message
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            # Show processing spinner
            with st.spinner("🔍 Analyzing and generating response..."):
                try:
                    workflow = get_workflow()
                    initial_state = {
                        "user_input": prompt,
                        "is_safe": False,
                        "classification": "",
                        "response": ""
                    }
                    final_state = workflow.invoke(initial_state)
                    response = final_state["response"]
                except Exception as e:
                    response = f"❌ Error: {str(e)}"
            
            # Add assistant response
            st.session_state.messages.append({"role": "assistant", "content": response})
            
            # Rerun to display the response
            st.rerun()

    # Sidebar with information
    with st.sidebar:
        st.header("ℹ️ About")
        st.markdown("""
        ### Security Features
        This AI system detects and alerts on:
        - 🚨 **Prompt Injection** - Direct attempts to override instructions
        - 🔗 **Indirect Prompt Injection** - Subtle manipulation attempts
        - 💾 **Data Poisoning** - Attempts to corrupt data
        - 📄 **Data Leakage** - Attempts to extract sensitive information

        ### How It Works
        1. You ask any question naturally
        2. The LLM analyzes for security threats
        3. Shows security status with the response
        4. Answers your question if safe

        ### Technology
        - **LLM**: Hugging Face (google/flan-t5-base)
        - **Framework**: LangChain + LangGraph
        - **Interface**: Streamlit
        - **Security**: LLM-based threat detection
        """)

        st.divider()
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🗑️ Clear Chat", use_container_width=True):
                st.session_state.messages = []
                st.session_state.processed_input = None
                st.rerun()
        
        with col2:
            if st.button("ℹ️ Help", use_container_width=True):
                st.info("Type your question and click Send. The AI will check for security threats and respond!")

if __name__ == "__main__":
    main()