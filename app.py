"""
Streamlit web interface for the Agentic AI Security System.
Provides a ChatGPT-like web interface for secure AI interactions with LangGraph workflow.
"""

import streamlit as st
from workflow import process_input
import time


# Configure page
st.set_page_config(
    page_title="Agentic AI Security System",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main {
        padding: 1rem;
    }
    .stChatMessage {
        padding: 1rem 0;
    }
    .chatbot-container {
        max-width: 1000px;
        margin: 0 auto;
        padding: 1rem 0;
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
        text-align: left;
    }
    .assistant-bubble {
        background: #f7f7f7;
        color: black;
        margin-right: auto;
        max-width: 100%;
        border: 1px solid #e5e5e5;
    }
    .security-safe {
        background: #f1f8e9;
        border-left: 4px solid #4caf50;
        padding: 12px;
        border-radius: 4px;
        margin: 8px 0;
    }
    .security-warning {
        background: #fff3e0;
        border-left: 4px solid #ff9800;
        padding: 12px;
        border-radius: 4px;
        margin: 8px 0;
    }
    .security-blocked {
        background: #ffebee;
        border-left: 4px solid #f44336;
        padding: 12px;
        border-radius: 4px;
        margin: 8px 0;
    }
    .workflow-info {
        background: #e3f2fd;
        border-left: 4px solid #2196f3;
        padding: 10px;
        border-radius: 4px;
        font-size: 0.85em;
        margin: 8px 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

if "show_workflow" not in st.session_state:
    st.session_state.show_workflow = False


def display_workflow_steps():
    """Display the agentic workflow steps."""
    st.markdown("""
    <div class="workflow-info">
    <strong>🔄 Agentic Workflow Enabled:</strong><br/>
    1. Input → 2. Analyze → 3. Security Check → 4. Validate → 5. RAG Retrieval → 6. Tool Execution → 7. Response
    </div>
    """, unsafe_allow_html=True)


def main():
    # Header
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(
            "<h1 style='text-align: center; color: #10a37f;'>🤖 Agentic AI Security System</h1>",
            unsafe_allow_html=True
        )
        st.markdown(
            "<p style='text-align: center; color: #666; font-size: 0.9em;'>Advanced AI with Multi-Step Security Analysis, RAG, and Tool Integration</p>",
            unsafe_allow_html=True
        )

    # Display workflow info if enabled
    if st.session_state.show_workflow:
        display_workflow_steps()

    # Chat display area
    with st.container():
        for message in st.session_state.messages:
            if message["role"] == "user":
                with st.chat_message("user"):
                    st.markdown(message["content"])
            else:
                with st.chat_message("assistant"):
                    st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("Ask me anything... (with security analysis)"):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.markdown(prompt)

        # Process through workflow
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            
            # Show processing steps
            with st.spinner("🔍 Processing through agentic workflow..."):
                try:
                    # Add small progress indicators
                    status_text = "🔄 Analyzing input..."
                    message_placeholder.markdown(status_text)
                    
                    # Process through LangGraph workflow
                    response = process_input(prompt)
                    
                    # Display response
                    message_placeholder.markdown(response)
                    
                except Exception as e:
                    error_msg = f"❌ **Error**: {str(e)}"
                    message_placeholder.markdown(error_msg)

        # Add assistant response to history
        st.session_state.messages.append({"role": "assistant", "content": response})

    # Sidebar information
    with st.sidebar:
        st.header("ℹ️ System Information")
        
        # Toggle workflow display
        st.session_state.show_workflow = st.checkbox(
            "Show workflow steps",
            value=st.session_state.show_workflow
        )
        
        st.divider()
        
        st.subheader("🔒 Security Detection")
        st.markdown("""
        This system detects:
        - **Prompt Injection** - Direct override attempts
        - **Indirect Injection** - Subtle manipulation
        - **Data Leakage** - Info extraction attempts
        - **Data Poisoning** - Corruption attempts
        """)

        st.divider()
        
        st.subheader("🛠️ Integrated Tools")
        st.markdown("""
        - **🔍 Search Tool** - Find information
        - **🧮 Calculator** - Math operations
        - **📄 File Reader** - Read local files
        """)

        st.divider()
        
        st.subheader("📊 RAG System")
        st.markdown("""
        Retrieval-Augmented Generation:
        - Loads documents from `/docs`
        - Retrieves relevant context
        - Enhances response accuracy
        """)

        st.divider()
        
        st.subheader("💾 Conversation Memory")
        st.markdown(f"""
        Current messages: **{len(st.session_state.messages)}**
        
        Memory keeps last 5 interactions
        for context in multi-turn conversations.
        """)

        st.divider()
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🗑️ Clear Chat", use_container_width=True):
                st.session_state.messages = []
                st.rerun()
        
        with col2:
            if st.button("🔄 Refresh", use_container_width=True):
                st.rerun()

        st.divider()
        
        st.markdown("""
        ### Technology Stack
        - **LLM**: Hugging Face (FLAN-T5)
        - **Framework**: LangChain + LangGraph
        - **RAG**: FAISS Vector Store
        - **Interface**: Streamlit
        - **API**: FastAPI (api.py)
        
        ### Project Structure
        - `workflow.py` - LangGraph workflow
        - `app.py` - Streamlit UI
        - `api.py` - FastAPI server
        - `llm/` - LLM integration
        - `security/` - Security detection
        - `rag/` - RAG pipeline
        - `tools/` - Tool implementations
        - `memory/` - Conversation memory
        """)


if __name__ == "__main__":
    main()
