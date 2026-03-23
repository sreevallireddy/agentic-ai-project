# Agentic AI Security System

A Python-based AI system with built-in security detection to prevent prompt injection and other security threats.

## Features

- **Security Detection**: Uses LLM-based classification to detect:
  - Prompt injection
  - Indirect prompt injection
  - Data leakage
  - Data poisoning
- **Safe Response Generation**: Only generates responses for safe inputs
- **Web Interface**: Streamlit-based chat interface
- **Modular Architecture**: Clean separation of concerns with LangGraph

## Requirements

- Python 3.8+
- Virtual environment support

## Setup Instructions

1. **Clone or navigate to the project directory:**
   ```bash
   cd /Users/sreevalli.ribm.com/agentic-ai-project
   ```

2. **Create a Python virtual environment:**
   ```bash
   python3 -m venv venv
   ```

3. **Activate the virtual environment:**
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## How to Run

### Web Interface (Recommended)
```bash
streamlit run app.py
```
This will open a web browser with the chat interface.

### Command Line Interface
```bash
python main.py
```

## Project Structure

```
agentic-ai-project/
├── app.py                  # Streamlit web interface
├── main.py                 # CLI application
├── workflow.py             # LangGraph definition with nodes/edges
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── security/
│   ├── __init__.py
│   └── detector.py        # Security threat detection logic
├── llm/
│   ├── __init__.py
│   └── model.py           # LangChain HuggingFace integration
├── utils/
│   ├── __init__.py
│   └── prompts.py         # Prompt templates and utilities
└── venv/                  # Virtual environment
```

## How It Works

1. **User Input**: User enters a query via web interface or CLI
2. **Security Check**: Input is analyzed by the LLM for security threats using LangGraph workflow
3. **Classification**: LLM classifies input into security categories or safe
4. **Response**:
   - If unsafe: Returns security warning
   - If safe: Generates AI response using the LLM

## Dependencies

- `transformers`: For Hugging Face model integration
- `torch`: PyTorch backend for transformers
- `langchain`: Framework for LLM applications
- `langchain-huggingface`: Hugging Face integration for LangChain
- `langgraph`: For workflow orchestration with nodes and edges
- `streamlit`: Web interface framework
- `python-dotenv`: Environment variable management

## Model

Uses `google/flan-t5-base` from Hugging Face, a free and accessible text-to-text generation model.

## Security Categories

- **prompt injection**: Direct attempts to override system prompts
- **indirect prompt injection**: Subtle manipulation attempts
- **data leakage**: Attempts to extract sensitive information
- **data poisoning**: Attempts to corrupt training data
- **safe**: No security threats detected

## Notes

- The first run may take longer as the model downloads
- Ensure stable internet connection for model loading
- The system uses CPU by default; GPU usage is automatic if available